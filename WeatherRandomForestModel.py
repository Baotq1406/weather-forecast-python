import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os

class WeatherRandomForestModel:
    def __init__(self, data_path):
        self.data_path = data_path
        self.df = None
        self.model = None

    def loadData(self):
        self.df = pd.read_csv(self.data_path)

    def split_data(self):
        # Nếu chưa có cột 'Date' kiểu datetime thì tạo lại
        if 'Date' not in self.df.columns or self.df['Date'].dtype != 'datetime64[ns]':
            self.df['Date'] = pd.to_datetime(self.df[['Year', 'Month', 'Day']])

        cutoff_date = pd.Timestamp('2023-12-31')

        train_df = self.df[self.df['Date'] <= cutoff_date].copy()
        test_df = self.df[self.df['Date'] > cutoff_date].copy()

        # Lấy tất cả các cột, loại bỏ cột ngày tháng
        date_cols = ['Day', 'Month', 'Year', 'DayOfWeek', 'Date']
        features = [col for col in self.df.columns if
                    col not in date_cols and col not in ['AverTemp_C', 'Precipitation_mm', 'AverHumidity_pct',
                                                         'AtmosPressure_hPa', 'WindSpeed_ms', 'SunDuration_hr']]

        # Đa đầu ra
        targets = ['AverTemp_C', 'Precipitation_mm', 'AverHumidity_pct',
                   'AtmosPressure_hPa', 'WindSpeed_ms', 'SunDuration_hr']

        X_train = train_df[features]
        y_train = train_df[targets]
        X_test = test_df[features]
        y_test = test_df[targets]

        print(f"Train size: {X_train.shape[0]} samples | Test size: {X_test.shape[0]} samples")
        return X_train, X_test, y_train, y_test

    def train(self, X_train, y_train):
        self.model = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)
        self.model.fit(X_train, y_train)
        print("Huấn luyện mô hình Random Forest xong.")

    def evaluate(self, X_test, y_test):
        y_pred = self.model.predict(X_test)

        if hasattr(y_test, 'columns'):
            target_names = y_test.columns
        else:
            target_names = [f"Target_{i}" for i in range(y_test.shape[1])]

        print("\nĐánh giá mô hình:")
        os.makedirs("prediction_plots", exist_ok=True)

        for i, target in enumerate(target_names):
            y_true_col = y_test.iloc[:, i].values
            y_pred_col = y_pred[:, i]

            mae = mean_absolute_error(y_true_col, y_pred_col)
            rmse = np.sqrt(mean_squared_error(y_true_col, y_pred_col))
            r2 = r2_score(y_true_col, y_pred_col)

            print(f"\n📌 [{target}]")
            print(f"  MAE : {mae:.2f}")
            print(f"  RMSE: {rmse:.2f}")
            print(f"  R2  : {r2:.2f}")

            plt.figure(figsize=(8, 4))
            plt.plot(y_true_col[:100], label='Thực tế', marker='o')
            plt.plot(y_pred_col[:100], label='Dự đoán', marker='x')
            plt.title(f'Dự đoán {target}')
            plt.xlabel('Sample Index')
            plt.ylabel(target)
            plt.legend()
            plt.tight_layout()
            plt.savefig(f"prediction_plots/{target}_prediction.png")
            plt.close()

        print("\n🖼️  Đã lưu các biểu đồ dự đoán trong thư mục prediction_plots")

    def save_model(self, model_path='rf_model_multi_output.pkl'):
        joblib.dump(self.model, model_path)
        print(f"✅ Đã lưu mô hình tại {model_path}.")

# Cách dùng
if __name__ == '__main__':
    model = WeatherRandomForestModel("data_features.csv")
    model.loadData()
    X_train, X_test, y_train, y_test = model.split_data()
    model.train(X_train, y_train)
    model.evaluate(X_test, y_test)
    model.save_model()
