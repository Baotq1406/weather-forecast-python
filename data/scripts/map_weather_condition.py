import pandas as pd

# Đọc file CSV, dùng raw string cho đường dẫn Windows
df = pd.read_csv(r'd:\Học Máy\weather-forecast-python_demo_01\data\processed\weather_data_processed.csv')

# Đảm bảo cột WeatherCondition là int (nếu bị string thì chuyển)
df['WeatherCondition'] = df['WeatherCondition'].astype(int)

# Từ điển mã WMO sang mô tả tiếng Anh
wmo_descriptions = {
    0: 'Clear sky',
    1: 'Mainly clear',
    2: 'Partly cloudy',
    3: 'Overcast',
    51: 'Drizzle: Light intensity',
    53: 'Drizzle: Moderate intensity',
    55: 'Drizzle: Dense intensity',
    61: 'Rain: Slight intensity',
    63: 'Rain: Moderate intensity',
    65: 'Rain: Heavy intensity',
}

# Ánh xạ mã sang mô tả
df['WeatherDescription'] = df['WeatherCondition'].map(wmo_descriptions)

# Thay giá trị NaN (mã không có trong từ điển) bằng 'Unknown'
df['WeatherDescription'].fillna('Unknown', inplace=True)

# Lưu file mới (dùng raw string)
df.to_csv(r'd:\Học Máy\weather-forecast-python_demo_01\data\processed\neo_weather_data_processed.csv', index=False)

# In ra bảng mã và mô tả không trùng
print(df[['WeatherCondition', 'WeatherDescription']].drop_duplicates().reset_index(drop=True))
