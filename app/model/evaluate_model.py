# Import các thư viện cần thiết
import pandas as pd  # Thư viện xử lý dữ liệu dạng bảng
import joblib  # Dùng để load mô hình đã lưu
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score  # Các hàm đánh giá mô hình
import os  # Thư viện xử lý đường dẫn và thư mục
import seaborn as sns  # Thư viện vẽ biểu đồ nâng cao
import matplotlib.pyplot as plt  # Thư viện vẽ biểu đồ cơ bản

# Định nghĩa hàm chính
def main():
    # Đường dẫn đến mô hình KNN đã huấn luyện
    model_path = r"D:\Học Máy\weather-forecast-python_demo_01\models\knn_model_05.pkl"
    
    # Đường dẫn chứa tập dữ liệu kiểm tra (test)
    test_data_dir = r"D:\Học Máy\weather-forecast-python_demo_01\data\test_data"
    
    # Đường dẫn để lưu báo cáo đánh giá (confusion matrix hình ảnh)
    save_dir = r"D:\Học Máy\weather-forecast-python_demo_01\classification_reports"

    # Tạo thư mục lưu nếu chưa tồn tại
    os.makedirs(save_dir, exist_ok=True)

    # Tải mô hình đã được lưu bằng joblib
    model = joblib.load(model_path)

    # Đọc dữ liệu kiểm tra (X_test: đặc trưng, y_test: nhãn thật)
    X_test = pd.read_csv(os.path.join(test_data_dir, "X_test.csv"))
    y_test = pd.read_csv(os.path.join(test_data_dir, "y_test.csv"))

    # Nếu y_test là DataFrame (có nhiều cột), chỉ lấy cột đầu tiên làm nhãn
    if isinstance(y_test, pd.DataFrame):
        y_test = y_test.iloc[:, 0]

    # Dự đoán nhãn bằng mô hình
    y_pred = model.predict(X_test)

    # In ra độ chính xác (accuracy) của mô hình
    print("Accuracy:", accuracy_score(y_test, y_pred))

    # In ra báo cáo phân loại chi tiết (Precision, Recall, F1-score)
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # Lấy danh sách nhãn phân loại (label) sắp xếp theo thứ tự để giữ tính nhất quán
    labels = sorted(y_test.unique())

    # Tính confusion matrix giữa nhãn thật và nhãn dự đoán
    cm = confusion_matrix(y_test, y_pred, labels=labels)

    # In confusion matrix dạng bảng (DataFrame) trên terminal
    cm_df = pd.DataFrame(cm, index=labels, columns=labels)
    print("\nConfusion Matrix:")
    print(cm_df)

    # Vẽ biểu đồ confusion matrix dạng heatmap
    plt.figure(figsize=(12, 10))  # Kích thước hình
    sns.heatmap(cm_df, annot=True, fmt="d", cmap="Blues")  # Tạo biểu đồ với số nguyên
    plt.xlabel("Predicted")  # Nhãn trục X
    plt.ylabel("Actual")  # Nhãn trục Y
    plt.title("Confusion Matrix")  # Tiêu đề biểu đồ
    plt.tight_layout()  # Căn chỉnh bố cục cho đẹp

    # Lưu biểu đồ confusion matrix dưới dạng hình ảnh
    save_path = os.path.join(save_dir, "confusion_matrix.png")
    plt.savefig(save_path)
    print(f"Confusion matrix saved to {save_path}")

    # Hiển thị biểu đồ trên màn hình
    plt.show()

# Nếu file này được chạy trực tiếp, gọi hàm main()
if __name__ == "__main__":
    main()
