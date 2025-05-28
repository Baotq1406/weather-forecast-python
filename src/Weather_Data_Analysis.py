import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates  # Thêm import này

# Đọc dữ liệu và xử lý như bạn có
df = pd.read_csv(r'D:\Học Máy\weather-forecast-python_demo_02\data\processed\weather_data_processed.csv')
df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
df['Date'] = df['DateTime'].dt.date
start_date = pd.to_datetime('2024-01-01')
end_date = pd.to_datetime('2024-12-31')
df = df[(df['DateTime'] >= start_date) & (df['DateTime'] <= end_date)]

daily = df.groupby('Date')['Temp_C'].agg(['min', 'max', 'mean'])
daily.rename(columns={'min': 'temp_min', 'max': 'temp_max', 'mean': 'temp_mean'}, inplace=True)
percentiles_25_75 = df.groupby('Date')['Temp_C'].agg(
    p25=lambda x: x.quantile(0.25),
    p75=lambda x: x.quantile(0.75)
)
percentiles_10_90 = df.groupby('Date')['Temp_C'].agg(
    p10=lambda x: x.quantile(0.10),
    p90=lambda x: x.quantile(0.90)
)
daily = daily.join(percentiles_25_75).join(percentiles_10_90)

plt.figure(figsize=(16, 8))
dates = pd.to_datetime(daily.index)
plt.bar(dates, daily['temp_max'] - daily['temp_min'], bottom=daily['temp_min'], color='gray', alpha=0.3, label='Phạm vi nhiệt độ (Min-Max)')
plt.plot(dates, daily['temp_max'], color='red', alpha=0.3, label='Nhiệt độ cao trung bình')
plt.plot(dates, daily['temp_min'], color='deepskyblue', alpha=0.3, label='Nhiệt độ thấp trung bình')
plt.fill_between(dates, daily['p25'], daily['p75'], color='red', alpha=0.1, label='Dải 25-75 percentiles')
plt.fill_between(dates, daily['p10'], daily['p90'], color='deepskyblue', alpha=0.1, label='Dải 10-90 percentiles')
plt.scatter(dates, daily['temp_max'], color='red', edgecolor='black', s=40, label='Nhiệt độ cao hàng ngày')
plt.scatter(dates, daily['temp_min'], color='deepskyblue', edgecolor='black', s=40, label='Nhiệt độ thấp hàng ngày')

# Thiết lập trục x hiển thị đầy đủ tháng
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.xticks(rotation=45)

plt.title('Phạm vi và nhiệt độ cao thấp hàng ngày từ 01/2024 đến 12/2024')
plt.xlabel('Ngày')
plt.ylabel('Nhiệt độ (°C)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
