import requests
import pandas as pd

# Tọa độ trung tâm tỉnh Quảng Nam
latitude = 15.5736
longitude = 108.4740

# Các thông số cần lấy: nhiệt độ, lượng mưa, độ ẩm, tốc độ gió, số giờ nắng, áp suất
parameters = [
    "T2M",                # Nhiệt độ trung bình (°C)
    "PRECTOTCORR",        # Lượng mưa (mm)
    "RH2M",               # Độ ẩm trung bình (%)
    "WS2M",               # Tốc độ gió tại 2m (m/s)
    "ALLSKY_SFC_SW_DWN",  # Bức xạ mặt trời (W/m^2) --> sẽ chuyển đổi ra giờ nắng xấp xỉ
    "PS"                  # Áp suất (hPa)
]

# Dải thời gian: 2015-01-01 đến 2023-12-31
start_date = "20150101"
end_date = "20241231"

# Gọi API
url = f"https://power.larc.nasa.gov/api/temporal/daily/point?parameters={','.join(parameters)}&community=AG&longitude={longitude}&latitude={latitude}&start={start_date}&end={end_date}&format=JSON"

response = requests.get(url)
data = response.json()

# Trích xuất dữ liệu
records = data['properties']['parameter']
dates = list(records['T2M'].keys())

# Chuyển bức xạ mặt trời (W/m^2) sang "giờ nắng xấp xỉ"
# 1 MJ/m² = 277.78 Wh/m² -> giả sử ngưỡng 120 W/m² là giờ nắng hiệu quả
sun_hours = [records["ALLSKY_SFC_SW_DWN"][d] / 120 for d in dates]

# Gộp dữ liệu vào DataFrame
df = pd.DataFrame({
    "Date": pd.to_datetime(dates),
    "AverTemp(°C)": [records["T2M"][d] for d in dates],
    "Precipitation(mm)": [records["PRECTOTCORR"][d] for d in dates],
    "AverHumidity(%)": [records["RH2M"][d] for d in dates],
    "WindSpeed(m/s)": [records["WS2M"][d] for d in dates],
    "SunDuration(giờ)": sun_hours,
    "AtmosPressure(hPa)": [records["PS"][d] for d in dates],
})

# Xuất file CSV
csv_path = "quangnam_weather_full_2019_2024.csv"
df.to_csv(csv_path, index=False)

weather_df = pd.read_csv("quangnam_weather_full_2019_2024.csv")
def classify_weather(row):
    labels = []
    if row['Precipitation(mm)'] > 5:
        labels.append("Mưa lớn")
    if row['AverTemp(°C)'] > 35 and row['SunDuration(giờ)'] > 6:
        labels.append("Nắng gắt")
    if row['AverTemp(°C)'] < 18:
        labels.append("Trời lạnh (<18°C)")
    if row['AverHumidity(%)'] > 90:
        labels.append("Độ ẩm cao")
    if row['WindSpeed(m/s)'] > 6:
        labels.append("Gió mạnh")
    return ", ".join(labels) if labels else "Bình thường"

# Bước 3: Áp dụng
weather_df["WeatherCondition"] = weather_df.apply(classify_weather, axis=1)

# Bước 4: Lưu lại nếu cần
weather_df.to_csv("weather_with_labels.csv", index=False)