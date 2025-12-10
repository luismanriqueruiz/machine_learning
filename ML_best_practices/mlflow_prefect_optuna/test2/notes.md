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

# Check simple test

```bash
python simple_test.py
```