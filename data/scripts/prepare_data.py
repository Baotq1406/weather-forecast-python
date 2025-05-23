import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Dùng raw string để tránh lỗi \n, \t,...
df = pd.read_csv(r'd:\Học Máy\weather-forecast-python\data\processed_data\weather_features.csv', parse_dates=['Date'])

df['Target_AverTemp'] = df['AverTemp(°C)'].shift(-1)
df = df[:-1]

y = df['Target_AverTemp']
X = df.drop(columns=['Date', 'Target_AverTemp', 'WeatherCondition'])

# Kiểm tra cột dạng object/string
categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
print("Categorical columns:", categorical_cols)

# One-hot encode các cột categorical nếu có
if categorical_cols:
    X = pd.get_dummies(X, columns=categorical_cols, drop_first=True)

# Chia train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, shuffle=False
)

# Scale dữ liệu
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Chuyển lại thành DataFrame cho dễ thao tác
X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns, index=X_train.index)
X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_test.columns, index=X_test.index)

print(f"Train set: {X_train_scaled.shape}, Test set: {X_test_scaled.shape}")

# Lưu dữ liệu đã chuẩn bị (đường dẫn tương đối hoặc tuyệt đối đều được)
X_train_scaled.to_csv(r'd:\Học Máy\weather-forecast-python\app\model\X_train_scaled.csv', index=False)
X_test_scaled.to_csv(r'd:\Học Máy\weather-forecast-python\app\model\X_test_scaled.csv', index=False)
y_train.to_frame(name='Target_AverTemp').to_csv(r'd:\Học Máy\weather-forecast-python\app\model\y_train.csv', index=False)
y_test.to_frame(name='Target_AverTemp').to_csv(r'd:\Học Máy\weather-forecast-python\app\model\y_test.csv', index=False)

print("✅ Hoàn thành chuẩn bị dữ liệu!")