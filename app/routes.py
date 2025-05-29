# routes.py

# Import các thư viện cần thiết từ Flask và thư viện ngoài
from flask import Blueprint, render_template, request  # Để xử lý tuyến đường (routes), render HTML và nhận dữ liệu từ form
import joblib  # Dùng để load mô hình đã lưu
import pandas as pd  # Dùng để xử lý dữ liệu đầu vào dưới dạng DataFrame

# Tạo một Blueprint để quản lý nhóm các route liên quan (tách riêng phần giao diện người dùng)
main = Blueprint('main', __name__)

# Đường dẫn đến mô hình học máy đã được huấn luyện và lưu bằng joblib
model_path = r"D:\Học Máy\weather-forecast-python_demo_01\models\knn_model_05.pkl"

# Load mô hình từ file
model = joblib.load(model_path)

# Định nghĩa một route cho trang chủ ('/') xử lý cả phương thức GET và POST
@main.route('/', methods=['GET', 'POST'])
def index():
    prediction = None  # Biến lưu kết quả dự đoán, mặc định là None
    selected_date = ''  # Biến lưu ngày được chọn từ form, mặc định rỗng

    # Nếu người dùng gửi biểu mẫu (POST)
    if request.method == 'POST':
        try:
            # Lấy dữ liệu ngày được nhập từ form
            selected_date = request.form['date']

            # Lấy các giá trị đầu vào từ form và chuyển sang kiểu float
            input_data = {
                'Temp_C': float(request.form['Temp_C']),  # Nhiệt độ (độ C)
                'Humidity_pct': float(request.form['Humidity_pct']),  # Độ ẩm (%)
                'Precipitation_mm': float(request.form['Precipitation_mm']),  # Lượng mưa (mm)
                'WindSpeed_kmh': float(request.form['WindSpeed_kmh']),  # Tốc độ gió (km/h)
                'CloudCover_pct': float(request.form['CloudCover_pct']),  # Mức độ mây che phủ (%)
                'AtmosPressure_hPa': float(request.form['AtmosPressure_hPa'])  # Áp suất khí quyển (hPa)
            }

            # Tạo một DataFrame từ dữ liệu đầu vào (phải có đúng định dạng mà mô hình yêu cầu)
            df = pd.DataFrame([input_data])

            # Dự đoán kết quả từ mô hình và lấy giá trị đầu tiên (do kết quả là một mảng)
            prediction = model.predict(df)[0]

        except Exception as e:
            # Nếu có lỗi xảy ra, gán thông báo lỗi cho biến prediction để hiển thị
            prediction = f"Lỗi: {e}"

    # Trả về template HTML kèm theo kết quả dự đoán và ngày đã chọn (nếu có)
    return render_template('index.html', prediction=prediction, selected_date=selected_date)
