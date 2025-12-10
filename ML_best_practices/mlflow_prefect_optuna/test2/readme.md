# Testing MLFlow + Prefect + Optuna

These experiments are testing MLflow for experiment tracking, Prefect for creating machine learning pipelines, and Optuna for hyperparameter tuning.

It consists in two parts:

# Example 1
## 1. Installing dependencies

```bash
pip install prefect mlflow optuna scikit-learn pandas numpy joblib imbalanced-learn
```

## 2. Run mlflow
```bash
mlflow ui
```

## 3. How it works

Prefect orchestrates:

- data simulation
    - train/test split
    - Optuna tuning
    - final training
    - model saving

- MLflow logs:
    - hyperparameters per Optuna trial
    - metrics (F1, ROC AUC)
    - best parameters
    - final trained model metrics

## 4. Run script

```bash
python churn_prefect_mlflow_optuna.py
```


# Example 2

This test will show how to implement the MLflow Model Registry with our churn model.

## Executing MLFlow
```bash
mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root ./mlflow_artifacts \
  --host 127.0.0.1 \
  --port 5000
```

## Running prefect locally

```bash
python churn_prefect_mlflow_optuna_v2.py
```

# Sanity test

Confirming MLflow works

```bash
python simple_test.py
```