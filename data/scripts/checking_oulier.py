import pandas as pd
import numpy as np
from scipy import stats

# 1. Đọc dữ liệu đã xử lý missing
df = pd.read_csv(r'd:\Học Máy\weather-forecast-python\data\processed_data\weather_filled_forward.csv')


# 2. Chọn các cột số để phát hiện outlier (bỏ cột Date, WeatherCondition)
numeric_cols = df.select_dtypes(include=[np.number]).columns

# --- Cách 1: Phát hiện outlier theo Z-score ---
z_scores = np.abs(stats.zscore(df[numeric_cols]))
threshold_z = 3
outliers_z = (z_scores > threshold_z)

# Tạo mask: dòng nào có ít nhất 1 outlier theo Z-score
mask_outlier_z = outliers_z.any(axis=1)

print(f"Số dòng có outlier theo Z-score: {mask_outlier_z.sum()}")

# --- Cách 2: Phát hiện outlier theo IQR ---
Q1 = df[numeric_cols].quantile(0.25)
Q3 = df[numeric_cols].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

mask_outlier_iqr = ((df[numeric_cols] < lower_bound) | (df[numeric_cols] > upper_bound)).any(axis=1)
print(f"Số dòng có outlier theo IQR: {mask_outlier_iqr.sum()}")

# --- Xử lý outlier ---

# Cách 1: Loại bỏ toàn bộ dòng có outlier (theo Z-score hoặc IQR)
df_no_outlier = df[~mask_outlier_z].copy()
# Nếu bạn muốn dùng IQR thì đổi mask_outlier_z thành mask_outlier_iqr

# Lưu file sau khi loại bỏ outlier
df_no_outlier.to_csv('d:\Học Máy\weather-forecast-python\data\processed_data\weather_no_outlier.csv', index=False)
print("Đã lưu file sau khi loại bỏ outlier: weather_no_outlier.csv")

# Cách 2: Thay thế outlier bằng giá trị trung vị (median) của cột

df_imputed = df.copy()
for col in numeric_cols:
    median_val = df[col].median()
    # Tìm vị trí outlier theo IQR (hoặc Z-score) ở cột col
    outlier_pos = (df[col] < lower_bound[col]) | (df[col] > upper_bound[col])
    # Thay outlier bằng median
    df_imputed.loc[outlier_pos, col] = median_val

# Lưu file sau khi thay thế outlier
df_imputed.to_csv('d:\Học Máy\weather-forecast-python\data\processed_data\weather_imputed_outlier.csv', index=False)
print("Đã lưu file sau khi thay thế outlier bằng median: weather_imputed_outlier.csv")
