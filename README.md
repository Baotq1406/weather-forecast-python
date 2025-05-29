1. File WeatherData.py : Lấy dữ liệu https://archive-api.open-meteo.com/v1/archive?
2. File QuangNam_Weather_Data.csv : Dữ liệu chưa xử lí
3. File PreprocessingData.py : Xử lí dữ liệu
4. File weather_data_processed.csv : Dữ liệu sạch
5. File WeatherStatistic.py : Buil trang web thống kê dữ liệu
    - Cài đặt thư viện streamlit, plotly, seaborn, ...
    - Vào Terminal : streamlit run WeatherStatistic.py
    - Không xoá phần code bị đánh dấu lại ( để sửa tiếp )
6. File WeatherRandomForestModel.py : Dùng model RandomForest để train ( File này chưa train được do dùng dữ liệu cũ )
