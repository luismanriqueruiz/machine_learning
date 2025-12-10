import mlflow
mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("chatbot_churn_prefect_optuna")

from prefect import flow, task, get_run_logger
import numpy as np
import pandas as pd
import optuna
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score, roc_auc_score
from imblearn.over_sampling import RandomOverSampler
import joblib
import os

RANDOM_SEED = 42
MLFLOW_EXPERIMENT_NAME = "chatbot_churn_prefect_optuna"
MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

# -------------------------------
# Data simulation
# -------------------------------
@task
def simulate_chatbot_churn_data(n_samples: int = 5000, churn_rate: float = 0.08):
    rng = np.random.RandomState(RANDOM_SEED)
    df = pd.DataFrame({
        "messages_count": rng.poisson(30, n_samples),
        "avg_response_time": rng.exponential(60, n_samples),
        "sessions_per_week": rng.poisson(3, n_samples),
        "sentiment_score": np.clip(rng.normal(0.2, 0.6, n_samples), -1, 1),
        "last_active_days": rng.exponential(25, n_samples),
        "used_premium_feature": rng.binomial(1, 0.12, n_samples),
        "had_recent_errors": rng.binomial(1, 0.07, n_samples)
    })

    # generate imbalanced churn target
    linear = (
        -0.04 * df["messages_count"] +
        0.01 * df["avg_response_time"] -
        0.3 * df["sessions_per_week"] -
        1.2 * df["sentiment_score"] +
        0.03 * df["last_active_days"] -
        0.8 * df["used_premium_feature"] +
        0.9 * df["had_recent_errors"]
    )
    probs = 1 / (1 + np.exp(-linear))
    probs = np.clip(probs * (0.08 / probs.mean()), 1e-6, 1 - 1e-6)

    df["churn"] = rng.binomial(1, probs)
    return df

# -------------------------------
# Split + balance
# -------------------------------
@task
def prepare_data(df: pd.DataFrame):
    X = df.drop(columns=["churn"])
    y = df["churn"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=RANDOM_SEED
    )

    ros = RandomOverSampler(random_state=RANDOM_SEED)
    X_train_bal, y_train_bal = ros.fit_resample(X_train, y_train)

    return X_train_bal, X_test, y_train_bal, y_test


# -------------------------------
# Optuna objective with MLflow (Bayesian optimization)
# -------------------------------
def objective(trial, X_train, y_train, X_test, y_test):
    n_estimators = trial.suggest_int("n_estimators", 100, 500)
    max_depth = trial.suggest_int("max_depth", 4, 20)
    min_samples_split = trial.suggest_int("min_samples_split", 2, 20)

    with mlflow.start_run(nested=True):
        model = Pipeline([
            ("scaler", StandardScaler()),
            ("clf", RandomForestClassifier(
                n_estimators=n_estimators,
                max_depth=max_depth,
                min_samples_split=min_samples_split,
                n_jobs=-1,
                random_state=RANDOM_SEED
            ))
        ])

        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        proba = model.predict_proba(X_test)[:, 1]

        f1 = f1_score(y_test, preds)
        auc = roc_auc_score(y_test, proba)

        # log to mlflow
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)
        mlflow.log_param("min_samples_split", min_samples_split)

        mlflow.log_metric("f1_score", f1)
        mlflow.log_metric("roc_auc", auc)

    return f1


# -------------------------------
# Hyperparameter tuning task
# -------------------------------
@task
def tune_hyperparameters(X_train, y_train, X_test, y_test, n_trials: int = 20):
    mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)

    with mlflow.start_run(run_name="optuna_hyperparameter_search"):
        study = optuna.create_study(direction="maximize")
        study.optimize(
            lambda trial: objective(trial, X_train, y_train, X_test, y_test),
            n_trials=n_trials
        )

        best_params = study.best_params
        best_score = study.best_value

        # log final best params
        mlflow.log_param("best_n_estimators", best_params["n_estimators"])
        mlflow.log_param("best_max_depth", best_params["max_depth"])
        mlflow.log_param("best_min_samples_split", best_params["min_samples_split"])
        mlflow.log_metric("best_f1_score", best_score)

    return best_params


# -------------------------------
# Train final model with best params
# -------------------------------
@task
def train_final_model(X_train, y_train, params):
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", RandomForestClassifier(
            **params,
            n_jobs=-1,
            random_state=RANDOM_SEED
        ))
    ])
    model.fit(X_train, y_train)
    return model


# -------------------------------
# Save + log model
# -------------------------------
@task
def save_and_log_model(model, X_test, y_test):
    preds = model.predict(X_test)
    proba = model.predict_proba(X_test)[:, 1]

    f1 = f1_score(y_test, preds)
    auc = roc_auc_score(y_test, proba)

    model_path = os.path.join(MODEL_DIR, "best_churn_model.joblib")
    joblib.dump(model, model_path)

    with mlflow.start_run(run_name="final_model"):
        mlflow.log_metric("final_f1_score", f1)
        mlflow.log_metric("final_roc_auc", auc)
        mlflow.log_artifact(model_path)

    return model_path, f1, auc


# -------------------------------
# Prefect Flow
# -------------------------------
@flow(name="churn-prefect-mlflow-optuna")
def churn_pipeline():
    logger = get_run_logger()

    df = simulate_chatbot_churn_data()
    X_train, X_test, y_train, y_test = prepare_data(df)

    best_params = tune_hyperparameters(X_train, y_train, X_test, y_test, n_trials=20)

    model = train_final_model(X_train, y_train, best_params)

    model_path, f1, auc = save_and_log_model(model, X_test, y_test)

    logger.info(f"✅ Best model saved to: {model_path}")
    logger.info(f"✅ Final F1: {f1:.4f}, ROC AUC: {auc:.4f}")

    return {
        "model_path": model_path,
        "f1_score": f1,
        "roc_auc": auc
    }


if __name__ == "__main__":
    churn_pipeline()
