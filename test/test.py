import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Đường dẫn file dữ liệu (bạn thay bằng đường dẫn thật của bạn)
file_path = r'd:\Học Máy\weather-forecast-python_demo_01\data\processed\neo_weather_data_processed.csv'

# Đọc dữ liệu
data = pd.read_csv(file_path)
data.columns = data.columns.str.strip()

# Chọn các cột số để PCA, bỏ Date, Time, CloudCover_pct
features = ["Temp_C", "Humidity_pct", "Precipitation_mm", "WindSpeed_kmh", "AtmosPressure_hPa"]
X = data[features]

# Chuẩn hóa dữ liệu trước PCA
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# PCA với 3 thành phần chính
pca = PCA(n_components=3)
X_pca = pca.fit_transform(X_scaled)

print("Tỷ lệ phương sai giải thích bởi các thành phần chính:", pca.explained_variance_ratio_)
print("Tổng tỷ lệ phương sai giữ lại:", sum(pca.explained_variance_ratio_))
print("Dữ liệu sau PCA (một vài dòng đầu):\n", X_pca[:5])
