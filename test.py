import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Load the saved model
model_path = r'd:\Học Máy\weather-forecast-python\models\knn_weather_model.pkl'
model = joblib.load(model_path)

# Load the scaler if you saved it (optional)
# scaler = joblib.load('path_to_scaler.pkl')

# Example: new data instances as a pandas DataFrame
new_data = pd.DataFrame([
    {
        'AverTemp(°C)': 27.5,
        'Precipitation(mm)': 5.0,
        'AverHumidity(%)': 80.0,
        'WindSpeed(m/s)': 3.0,
        'SunDuration(giờ)': 0.15,
        'AtmosPressure(hPa)': 100.5,
        'Year': 2025,
        'Month': 5,
        'Day': 23,
        'DayOfWeek': 4,
        'IsWeekend': 0,
        'Season_Mùa mưa': 1  # One-hot encoded season column
    }
])

# Ensure the columns match the training set
expected_columns = [
    'AverTemp(°C)', 'Precipitation(mm)', 'AverHumidity(%)', 'WindSpeed(m/s)',
    'SunDuration(giờ)', 'AtmosPressure(hPa)', 'Year', 'Month', 'Day',
    'DayOfWeek', 'IsWeekend', 'Season_Mùa mưa'
]

# Add missing columns if any (set to 0)
for col in expected_columns:
    if col not in new_data.columns:
        new_data[col] = 0

# Reorder columns to match model input
new_data = new_data[expected_columns]

# Optional: Apply the same scaler used in training if necessary
# Example (uncomment and edit if you saved the scaler):
# scaler = joblib.load(r'd:\Học Máy\weather-forecast-python\models\scaler.pkl')
# new_data = scaler.transform(new_data)

# Predict using the loaded model
predictions = model.predict(new_data)

print("Predicted values:", predictions)
