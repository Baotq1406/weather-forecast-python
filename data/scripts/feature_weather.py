import pandas as pd

# Đọc dữ liệu
df = pd.read_csv("d:\Học Máy\weather-forecast-python\data\processed_data\weather_no_outlier.csv")

# Đảm bảo cột Date là kiểu datetime
df['Date'] = pd.to_datetime(df['Date'])

# Trích xuất các đặc trưng thời gian
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day
df['DayOfWeek'] = df['Date'].dt.dayofweek  # 0: Monday, 6: Sunday
df['IsWeekend'] = df['DayOfWeek'].isin([5, 6]).astype(int)

# Tạo đặc trưng "Mùa vụ" (ở Miền trung (Quảng Nam, Đà Nẵng) thường chia theo tháng)
def get_season(month):
    if month in [9, 10, 11, 12]:
        return 'Mùa mưa'
    else:
        return 'Mùa khô'

df['Season'] = df['Month'].apply(get_season)

# Kiểm tra kết quả
print(df[['Date', 'Month', 'DayOfWeek', 'IsWeekend', 'Season']].head())

# Lưu lại DataFrame đã thêm các đặc trưng mới
df.to_csv("d:\Học Máy\weather-forecast-python\data\processed_data\weather_features.csv", index=False)
