import pandas as pd
import numpy as np
import os

# 1. Đọc file CSV gốc
df = pd.read_csv(r'd:\Học Máy\weather-forecast-python\data\weather_with_labels.csv')

# 2. Hàm tạo missing values ngẫu nhiên, không làm mất dữ liệu cột ngày
def add_random_missing_values(df, missing_fraction=0.1, random_seed=42, exclude_columns=None):
    np.random.seed(random_seed)
    df_with_nan = df.copy()
    numeric_cols = df_with_nan.select_dtypes(include=['float64', 'int64']).columns
    
    if exclude_columns is None:
        exclude_columns = []
    
    numeric_cols = [col for col in numeric_cols if col not in exclude_columns]
    
    for col in numeric_cols:
        n_missing = int(len(df_with_nan) * missing_fraction)
        missing_indices = np.random.choice(df_with_nan.index, n_missing, replace=False)
        df_with_nan.loc[missing_indices, col] = np.nan
    return df_with_nan

# 3. Thêm missing values (10%), loại trừ cột 'Date'
df_missing = add_random_missing_values(df, missing_fraction=0.1, exclude_columns=['Date'])

# 4. In số lượng missing sau khi thêm
print("Số lượng missing values theo cột sau khi thêm missing ngẫu nhiên:")
print(df_missing.isnull().sum())

# 5. Đường dẫn lưu file
output_dir = r'd:\Học Máy\weather-forecast-python\data\raw_data'
output_path = os.path.join(output_dir, 'weather_with_labels_with_missing.csv')

# 6. Tạo thư mục nếu chưa có
os.makedirs(output_dir, exist_ok=True)

# 7. Lưu file
df_missing.to_csv(output_path, index=False)
print(f"Đã lưu file dữ liệu mới có missing tại: {output_path}")
