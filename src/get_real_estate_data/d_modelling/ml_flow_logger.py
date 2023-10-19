##
import mlflow
import mlflow.sklearn

from src.get_real_estate_data.d_modelling.metrics import Metrics


def log_model(model, model_name, X_train, y_train, X_test, y_test):
    with mlflow.start_run():
        metrics_obj = Metrics(model, X_train, y_train, X_test, y_test)
        metrics_obj.report()

        mlflow.log_param("model", model_name)
        mlflow.log_params(model.get_params())

        # Log metrics
        mean_rmse_cv_score, std_rmse_cv_score = metrics_obj.cross_val_rmse()
        rmse = metrics_obj.test_rmse()
        mape = metrics_obj.test_mape()

        mlflow.log_metric("mean_rmse_cv_score", mean_rmse_cv_score)
        mlflow.log_metric("std_rmse_cv_score", std_rmse_cv_score)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mape", mape)

        # Log feature names
        feature_names = list(X_train.columns)
        mlflow.log_param("feature_names", feature_names)

        # Log the number of rows in X_train and X_test
        mlflow.log_param("X_train_rows", len(X_train))
        mlflow.log_param("X_test_rows", len(X_test))

        mlflow.sklearn.log_model(model, model_name)
