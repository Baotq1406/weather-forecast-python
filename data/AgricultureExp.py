import pandas as pd
import random

# Tập các giá trị đa dạng để tổ hợp thành 5000 kinh nghiệm KHÁC NHAU
crops = [
    "Lúa", "Ngô", "Rau màu", "Đậu phụng", "Cà chua", "Ớt", "Chuối", "Thanh long",
    "Mía", "Cà tím", "Dưa hấu", "Dưa leo", "Cải bẹ", "Bắp cải", "Xoài", "Sắn"
]

weather_conditions = [
    "Mưa lớn", "Mưa rào nhẹ", "Nắng gắt", "Trời âm u", "Sương mù dày", "Gió mạnh",
    "Nhiệt độ cao > 35°C", "Nhiệt độ thấp < 15°C", "Độ ẩm không khí cao", "Độ ẩm thấp",
    "Có áp thấp nhiệt đới", "Nắng nhẹ sau mưa", "Nhiều ngày nắng", "Trời nhiều mây",
    "Trời lạnh buổi sáng", "Nhiệt độ dao động mạnh trong ngày"
]

actions = [
    "Trì hoãn gieo trồng", "Tưới nước định kỳ", "Phun thuốc phòng bệnh", "Che phủ rơm/gỗ mục",
    "Tăng cường thoát nước", "Bón phân hữu cơ", "Tưới nhỏ giọt", "Dừng bón phân đạm",
    "Tỉa thưa cây con", "Phun chế phẩm sinh học", "Đào mương xung quanh ruộng",
    "Bắt sâu thủ công", "Che chắn bằng lưới", "Theo dõi sát thời tiết", "Gieo trồng sớm hơn 5 ngày",
    "Bón vôi cải tạo đất"
]

# Mô tả chi tiết dựa theo logic của thời tiết và hành động
description_templates = [
    "Giúp cây tránh {problem}",
    "Giảm nguy cơ {problem}",
    "Bảo vệ cây khỏi {problem}",
    "Hạn chế ảnh hưởng của {problem}",
    "Tăng khả năng chống chịu với {problem}"
]

problems = [
    "thối rễ", "héo rũ", "nấm bệnh", "đạo ôn", "cháy lá", "sâu xanh", "bạc lá",
    "ngập úng", "thiếu nước", "sốc nhiệt", "rụng hoa", "nảy mầm kém", "suy kiệt", "vàng lá"
]

# Sinh dữ liệu
unique_experiences = set()
rows = []

while len(rows) < 5000:
    crop = random.choice(crops)
    weather = random.choice(weather_conditions)
    action = random.choice(actions)
    problem = random.choice(problems)
    description_template = random.choice(description_templates)
    description = description_template.format(problem=problem)

    row = (crop, weather, action, description)

    # Dùng set để đảm bảo không trùng lặp
    if row not in unique_experiences:
        unique_experiences.add(row)
        rows.append(row)

# Tạo DataFrame
df = pd.DataFrame(rows, columns=["Loại cây trồng", "Điều kiện thời tiết", "Hành động khuyến nghị", "Mô tả chi tiết"])

# Lưu file CSV
file_path = "kinh_nghiem_thoi_tiet_5000_unique.csv"
df.to_csv(file_path, index=False)