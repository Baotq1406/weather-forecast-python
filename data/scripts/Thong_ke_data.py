import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Đọc dữ liệu đã xử lý outlier
df = pd.read_csv("d:\Học Máy\weather-forecast-python\data\processed_data\weather_no_outlier.csv")

# Hiển thị thống kê mô tả
print("\n📊 Thống kê mô tả sau khi xử lý outlier:\n")
print(df.describe())

# Danh sách các cột số
numeric_cols = ['AverTemp(°C)', 'Precipitation(mm)', 'AverHumidity(%)',
                'WindSpeed(m/s)', 'SunDuration(giờ)', 'AtmosPressure(hPa)']

# Vẽ Boxplot
print("\n📦 Biểu đồ Boxplot từng cột:\n")
for col in numeric_cols:
    plt.figure(figsize=(6, 1.5))
    sns.boxplot(data=df, x=col, color='skyblue')
    plt.title(f'Boxplot - {col}')
    plt.tight_layout()
    plt.show()

# Vẽ Histogram
print("\n📈 Biểu đồ Histogram từng cột:\n")
for col in numeric_cols:
    plt.figure(figsize=(6, 3))
    sns.histplot(data=df, x=col, kde=True, bins=30, color='orange')
    plt.title(f'Histogram - {col}')
    plt.tight_layout()
    plt.show()
