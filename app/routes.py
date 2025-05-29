from flask import Blueprint, render_template, request, jsonify
import joblib
import pandas as pd

main = Blueprint('main', __name__)

model_path = r"D:\Học Máy\weather-forecast-python_demo_01\models\knn_model_05.pkl"
model = joblib.load(model_path)

@main.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    selected_date = ''

    if request.method == 'POST':
        try:
            selected_date = request.form['date']
            input_data = {
                'Temp_C': float(request.form['Temp_C']),
                'Humidity_pct': float(request.form['Humidity_pct']),
                'Precipitation_mm': float(request.form['Precipitation_mm']),
                'WindSpeed_kmh': float(request.form['WindSpeed_kmh']),
                'CloudCover_pct': float(request.form['CloudCover_pct']),
                'AtmosPressure_hPa': float(request.form['AtmosPressure_hPa'])
            }
            df = pd.DataFrame([input_data])
            prediction = model.predict(df)[0]
        except Exception as e:
            prediction = f"Lỗi: {e}"

    return render_template('index.html', prediction=prediction, selected_date=selected_date)

@main.route('/api/predict', methods=['POST'])
def api_predict():
    try:
        data = request.get_json(force=True)  # force=True giúp đọc JSON ngay cả khi header Content-Type sai (cẩn thận dùng)

        if data is None:
            return jsonify({'error': 'No JSON data received'}), 400

        # Kiểm tra đầy đủ trường
        required_fields = ['Temp_C', 'Humidity_pct', 'Precipitation_mm', 'WindSpeed_kmh', 'CloudCover_pct', 'AtmosPressure_hPa']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

        input_data = {field: float(data[field]) for field in required_fields}
        df = pd.DataFrame([input_data])
        prediction = model.predict(df)[0]

        return jsonify({'prediction': prediction})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
