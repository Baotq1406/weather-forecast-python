import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib  # để lưu mô hình
import os

def main():
    file_path = r'd:\Học Máy\weather-forecast-python_demo_01\data\processed\neo_weather_data_processed.csv'

    # Đường dẫn thư mục lưu mô hình và dữ liệu test
    model_dir = r'D:\Học Máy\weather-forecast-python_demo_01\models'
    test_data_dir = r'D:\Học Máy\weather-forecast-python_demo_01\data\test_data'

    # Tạo thư mục nếu chưa tồn tại
    os.makedirs(model_dir, exist_ok=True)
    os.makedirs(test_data_dir, exist_ok=True)

    data = pd.read_csv(file_path)
    data.columns = data.columns.str.strip()

    # Loại bỏ cột 'CloudCover_pct' cùng với các cột không cần thiết khác
    y = data["WeatherDescription"]
    X = data.drop(columns=["Date", "Time", "WeatherCondition", "WeatherDescription"])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y)

    # Khởi tạo và huấn luyện mô hình Random Forest
    model = RandomForestClassifier(n_estimators=100, random_state=42)  # n_estimators có thể thay đổi tùy theo bạn
    model.fit(X_train, y_train)

    # Lưu mô hình và dữ liệu test để evaluate sau
    joblib.dump(model, os.path.join(model_dir, "random_forest_model_04.pkl"))
    X_test.to_csv(os.path.join(test_data_dir, "X_test.csv"), index=False)
    y_test.to_csv(os.path.join(test_data_dir, "y_test.csv"), index=False)

    print("Training complete. Random Forest model and test data saved.")

if __name__ == "__main__":
    main()
