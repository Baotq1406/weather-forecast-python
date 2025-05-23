import pandas as pd

# Đọc dữ liệu
df = pd.read_csv(r'd:\Học Máy\weather-forecast-python\data\raw_data\weather_with_labels_with_missing.csv')


# Kiểm tra missing data trước khi xử lý
print("Missing data trước khi điền:")
print(df.isnull().sum())

# Điền giá trị missing bằng phương pháp forward fill (giá trị trước đó)
df_ffill = df.fillna(method='ffill')

# Nếu vẫn còn missing data ở đầu bảng (do không có giá trị trước đó để điền), bạn có thể dùng backward fill tiếp
df_ffill = df_ffill.fillna(method='bfill')

# Kiểm tra missing data sau khi xử lý
print("Missing data sau khi điền:")
print(df_ffill.isnull().sum())

# Lưu dữ liệu đã xử lý ra file mới
df_ffill.to_csv('d:\Học Máy\weather-forecast-python\data\processed_data\weather_filled_forward.csv', index=False)
