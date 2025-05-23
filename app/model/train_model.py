import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
import joblib

# Load dữ liệu train đã chuẩn hóa từ file CSV
X_train_scaled = pd.read_csv(r'd:\Học Máy\weather-forecast-python\app\model\X_train_scaled.csv')
y_train = pd.read_csv(r'd:\Học Máy\weather-forecast-python\app\model\y_train.csv')['Target_AverTemp']

# Khởi tạo mô hình KNN
knn = KNeighborsRegressor(n_neighbors=5)

# Huấn luyện mô hình
knn.fit(X_train_scaled, y_train)

# Lưu mô hình
joblib.dump(knn, r'd:\Học Máy\weather-forecast-python\models\knn_weather_model.pkl')

print("✅ Mô hình KNN đã được lưu!")
