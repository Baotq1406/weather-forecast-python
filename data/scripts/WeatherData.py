import requests
import pandas as pd

latitude = 15.5736
longitude = 108.4740

start_date = '2020-01-01'
end_date = '2024-12-31'

hourly_params = [
    'temperature_2m',
    'relative_humidity_2m',
    'precipitation',
    'windspeed_10m',
    'cloudcover',
    'pressure_msl',
    'weathercode'
]

url = (
    f'https://archive-api.open-meteo.com/v1/archive?'
    f'latitude={latitude}&longitude={longitude}'
    f'&start_date={start_date}&end_date={end_date}'
    f'&hourly={",".join(hourly_params)}'
    f'&timezone=Asia%2FHo_Chi_Minh'
)

response = requests.get(url)
data = response.json()

df = pd.DataFrame(data['hourly'])
df['time'] = pd.to_datetime(df['time'])

# Lọc lấy mỗi 3h
df = df[df['time'].dt.hour % 3 == 0].reset_index(drop=True)

# Tách thành cột Date và Time riêng
df['Date'] = df['time'].dt.date.astype(str)    # YYYY-MM-DD dạng string
df['Time'] = df['time'].dt.strftime('%H:%M')  # hh:mm dạng string

# Bỏ cột gốc datetime đi cho gọn
df = df.drop(columns=['time'])

# Sắp xếp lại cột, Date và Time lên trước
cols = ['Date', 'Time'] + [col for col in df.columns if col not in ['Date', 'Time']]
df = df[cols]

df.rename(columns = {
    'temperature_2m':'Temp_C',
    'relative_humidity_2m': "Humidity_pct",
    'precipitation': 'Precipitation_mm',
    'windspeed_10m': 'WindSpeed_kmh',
    'cloudcover': "CloudCover_pct",
    'pressure_msl': 'AtmosPressure_hPa',
    'weathercode' : 'WeatherCondition'
}, inplace = True)
df.to_csv('QuangNam_Weather_Data.csv', index=False)
print("Đã lưu file")
