# Import lớp Flask từ thư viện Flask
from flask import Flask

# Hàm tạo và cấu hình ứng dụng Flask
def create_app():
    # Khởi tạo một đối tượng Flask, đại diện cho ứng dụng web
    app = Flask(__name__)

    # Import Blueprint 'main' từ module routes (tập tin routes.py trong cùng package)
    from .routes import main

    # Đăng ký Blueprint 'main' vào ứng dụng Flask
    # Blueprint giúp chia nhỏ cấu trúc ứng dụng thành các phần có thể tái sử dụng và quản lý độc lập
    app.register_blueprint(main)

    # Trả về đối tượng app đã được cấu hình, sẵn sàng để chạy
    return app
