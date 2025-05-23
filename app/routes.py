from flask import Blueprint, request, render_template
import pandas as pd
import joblib

main = Blueprint('main', __name__)

# Load mô hình
model = joblib.load(r'd:\Học Máy\weather-forecast-python\models\knn_weather_model.pkl')

@main.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    if request.method == 'POST':
        # Lấy dữ liệu form
        input_data = {
            'AverTemp(°C)': float(request.form['AverTemp']),
            'Precipitation(mm)': float(request.form['Precipitation']),
            'AverHumidity(%)': float(request.form['Humidity']),
            'WindSpeed(m/s)': float(request.form['WindSpeed']),
            'SunDuration(giờ)': float(request.form['SunDuration']),
            'AtmosPressure(hPa)': float(request.form['Pressure']),
            'Year': int(request.form['Year']),
            'Month': int(request.form['Month']),
            'Day': int(request.form['Day']),
            'DayOfWeek': int(request.form['DayOfWeek']),
            'IsWeekend': int(request.form['IsWeekend']),
            'Season_Mùa mưa': 1 if request.form['Season'] == 'rainy' else 0
        }

        expected_columns = [
            'AverTemp(°C)', 'Precipitation(mm)', 'AverHumidity(%)', 'WindSpeed(m/s)',
            'SunDuration(giờ)', 'AtmosPressure(hPa)', 'Year', 'Month', 'Day',
            'DayOfWeek', 'IsWeekend', 'Season_Mùa mưa'
        ]

        df = pd.DataFrame([input_data])

        # Thêm các cột thiếu (nếu có)
        for col in expected_columns:
            if col not in df.columns:
                df[col] = 0

        df = df[expected_columns]

        # Dự đoán
        prediction = model.predict(df)[0]

    return render_template('index.html', prediction=prediction)
