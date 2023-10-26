import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score


class Metrics:
    def __init__(self, model, X_train, y_train, X_test, y_test, cv=5):
        self.model = model
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        self.cv = cv
        self.y_pred = None

    def cross_val_rmse(self):
        cv_scores = cross_val_score(
            self.model, self.X_train, self.y_train, cv=self.cv, scoring='neg_mean_squared_error'
        )
        rmse_cv_scores = np.sqrt(-cv_scores)
        mean_rmse_cv_score = np.mean(rmse_cv_scores)
        std_rmse_cv_score = np.std(rmse_cv_scores)
        return mean_rmse_cv_score, std_rmse_cv_score

    @staticmethod
    def _mean_absolute_percentage_error(y_true, y_pred):
        y_true, y_pred = np.array(y_true), np.array(y_pred)
        return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

    def _fit_and_predict(self):
        self.model.fit(self.X_train, self.y_train)
        self.y_pred = self.model.predict(self.X_test)

    def test_rmse(self):
        rmse = np.sqrt(mean_squared_error(self.y_test, self.y_pred))
        return rmse

    def test_mape(self):
        mape = self._mean_absolute_percentage_error(self.y_test, self.y_pred)
        return mape

    def plot_residuals(self):
        residuals = self.y_test - self.y_pred
        sns.scatterplot(x=self.y_pred, y=residuals, alpha=0.5)
        plt.xlabel('Predicted Values')
        plt.ylabel('Residuals')
        plt.title('Residuals vs. Predicted Values')
        plt.axhline(y=0, color='r', linestyle='--')
        plt.show()

    def plot_true_vs_predicted(self):
        sns.scatterplot(x=self.y_test, y=self.y_pred, alpha=0.5)
        plt.xlabel('True Values')
        plt.ylabel('Predicted Values')
        plt.title('True Values vs. Predicted Values')
        plt.plot([self.y_test.min(), self.y_test.max()], [self.y_test.min(), self.y_test.max()], 'k--', lw=2)
        plt.show()

    def report(self):
        self._fit_and_predict()
        mean_rmse_cv_score, std_rmse_cv_score = self.cross_val_rmse()
        print(f"Mean RMSE CV Score on Train Data: {mean_rmse_cv_score:.4f}, Std. Dev: {std_rmse_cv_score:.4f}")
        rmse = self.test_rmse()
        print(f"Root Mean Squared Error on Test Data: {rmse:.4f}")
        mape = self.test_mape()
        print(f"Mean Absolute Percentage Error on Test Data: {mape:.4f}%")
