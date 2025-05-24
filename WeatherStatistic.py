# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import plotly.express as px
# import plotly.graph_objects as go
#
# # Hàm load data cache ngoài class
# @st.cache_data
# def load_data(filepath):
#     df = pd.read_csv(filepath)
#     df['Date'] = pd.to_datetime(df['Date'])
#     df['Year'] = df['Date'].dt.year
#     df['Month'] = df['Date'].dt.month
#     df['Day'] = df['Date'].dt.day
#     return df
#
# class WeatherAnalyzer:
#     def __init__(self, df):
#         self.df = df
#
#     def show_WeatherStatistics(self):
#         df = self.df
#         st.title("📊 Thống Kê Nhiệt Độ - Độ Ẩm - Lượng Mưa Tỉnh Quảng Nam (2020-2024)")
#
#         # 1. Trung bình nhiệt độ, lượng mưa, độ ẩm theo tháng của từng năm
#         st.header("1️⃣ Trung Bình Tháng: Nhiệt Độ, Lượng Mưa và Độ Ẩm Theo Từng Năm")
#
#         # Tính trung bình theo tháng và năm
#         monthly_avg = df.groupby(['Year', 'Month']).agg({
#             'Temp_C': 'mean',
#             'Precipitation_mm': 'mean',
#             'Humidity_pct': 'mean'
#         }).reset_index()
#
#         # Hàm vẽ biểu đồ line với nhiều năm
#         def plot_monthly_lines(data, value_col, title, y_label):
#             import plotly.graph_objects as go
#             import plotly.colors as pc
#
#             years = sorted(data['Year'].unique())
#             month_range = list(range(1, 13))
#
#             # Chọn 5 màu khác biệt rõ ràng cho 5 năm
#             colors = pc.qualitative.Dark24[:len(years)]
#
#             fig = go.Figure()
#             for i, year in enumerate(years):
#                 year_data = data[data['Year'] == year]
#                 # Đảm bảo đủ 12 tháng, nếu thiếu thì NaN để line ko đứt đoạn
#                 y_vals = [
#                     year_data[year_data['Month'] == m][value_col].values[0] if m in year_data['Month'].values else None
#                     for m in month_range]
#                 fig.add_trace(go.Scatter(
#                     x=month_range,
#                     y=y_vals,
#                     mode='lines+markers',
#                     name=str(year),
#                     line=dict(color=colors[i], width=3),
#                     marker=dict(size=6)
#                 ))
#
#             fig.update_layout(
#                 title=title,
#                 xaxis_title='Tháng',
#                 yaxis_title=y_label,
#                 xaxis=dict(tickmode='linear', tick0=1, dtick=1),
#                 height=400,
#                 legend_title='Năm'
#             )
#             return fig
#
#         # Hiển thị 3 biểu đồ cùng 1 hàng
#         col1, col2, col3 = st.columns(3)
#
#         with col1:
#             st.plotly_chart(
#                 plot_monthly_lines(monthly_avg, 'Temp_C', '🌡️ Nhiệt Độ Trung Bình Theo Tháng', 'Nhiệt độ (°C)'),
#                 use_container_width=True
#             )
#
#         with col2:
#             st.plotly_chart(
#                 plot_monthly_lines(monthly_avg, 'Precipitation_mm', '🌧️ Lượng Mưa Trung Bình Theo Tháng',
#                                    'Lượng mưa (mm)'),
#                 use_container_width=True
#             )
#
#         with col3:
#             st.plotly_chart(
#                 plot_monthly_lines(monthly_avg, 'Humidity_pct', '💧 Độ Ẩm Trung Bình Theo Tháng', 'Độ ẩm (%)'),
#                 use_container_width=True
#             )
#
#         # 2. Tổng kết trung bình 5 năm và theo tháng trong 5 năm
#         st.header("2️⃣ Tổng Kết Trung Bình 5 Năm")
#
#         avg_5year = df[['Temp_C', 'Precipitation_mm', 'Humidity_pct']].mean()
#         st.markdown(
#             f"""- **Trung bình toàn kỳ 5 năm:**
#             🌡️ Nhiệt độ: **{avg_5year['Temp_C']:.2f}°C**
#             🌧️ Lượng mưa: **{avg_5year['Precipitation_mm']:.2f} mm**
#             💧 Độ ẩm: **{avg_5year['Humidity_pct']:.2f}%**"""
#         )
#
#         monthly_avg_5year = df.groupby('Month')[['Temp_C', 'Precipitation_mm', 'Humidity_pct']].mean().reset_index()
#
#         # --- Vẽ biểu đồ bar màu tương tác ---
#         def plot_colored_bar(monthly_avg_df, column, title, unit, palette):
#             import plotly.graph_objects as go
#             import seaborn as sns
#
#             colors = sns.color_palette(palette, 12).as_hex()
#             sorted_months = monthly_avg_df.sort_values(by=column)['Month'].tolist()
#             color_map = {month: color for month, color in zip(sorted_months, colors)}
#
#             fig = go.Figure()
#             for _, row in monthly_avg_df.iterrows():
#                 fig.add_trace(go.Bar(
#                     x=[row['Month']],
#                     y=[row[column]],
#                     text=f"{row[column]:.1f} {unit}",
#                     textposition="inside",
#                     marker_color=color_map[row['Month']],
#                     name=str(row['Month']),
#                 ))
#
#             fig.update_layout(
#                 title=title,
#                 xaxis_title="Tháng",
#                 yaxis_title=f"{column} ({unit})",
#                 showlegend=False,
#                 height=400
#             )
#             return fig
#
#         # --- Hiển thị 3 biểu đồ trong cùng 1 hàng ---
#         col1, col2, col3 = st.columns(3)
#
#         with col1:
#             st.plotly_chart(
#                 plot_colored_bar(monthly_avg_5year, "Temp_C", "🌡 Nhiệt Độ Trung Bình Theo Tháng", "°C", "OrRd"),
#                 use_container_width=True
#             )
#
#         with col2:
#             st.plotly_chart(
#                 plot_colored_bar(monthly_avg_5year, "Precipitation_mm", "🌧️ Lượng Mưa Trung Bình Theo Tháng", "mm",
#                                  "Blues"),
#                 use_container_width=True
#             )
#
#         with col3:
#             st.plotly_chart(
#                 plot_colored_bar(monthly_avg_5year, "Humidity_pct", "💧 Độ Ẩm Trung Bình Theo Tháng", "%", "Greens"),
#                 use_container_width=True
#             )
#
#         # 3. Năm nào nóng nhất, tháng nóng nhất/lạnh nhất (cùng lượng mưa và độ ẩm)
#         st.header("3️⃣ Năm và Tháng Nóng/Lạnh Nhất")
#
#         avg_year_temp = df.groupby('Year')['Temp_C'].mean()
#         hottest_year = avg_year_temp.idxmax()
#         coldest_year = avg_year_temp.idxmin()
#         st.write(f"- Năm nóng nhất: **{hottest_year}** với nhiệt độ trung bình {avg_year_temp[hottest_year]:.2f}°C")
#         st.write(f"- Năm lạnh nhất: **{coldest_year}** với nhiệt độ trung bình {avg_year_temp[coldest_year]:.2f}°C")
#
#         avg_month_temp = df.groupby(['Year', 'Month'])['Temp_C'].mean()
#         hottest_month = avg_month_temp.idxmax()
#         coldest_month = avg_month_temp.idxmin()
#
#         # Lấy luôn mưa và ẩm tháng đó
#         def get_precip_hum(year, month):
#             sub = df[(df['Year'] == year) & (df['Month'] == month)]
#             return sub['Precipitation_mm'].mean(), sub['Humidity_pct'].mean()
#
#         hot_precip, hot_hum = get_precip_hum(*hottest_month)
#         cold_precip, cold_hum = get_precip_hum(*coldest_month)
#
#         st.write(
#             f"- Tháng nóng nhất: **{hottest_month[1]}/{hottest_month[0]}** với nhiệt độ trung bình {avg_month_temp[hottest_month]:.2f}°C, lượng mưa trung bình {hot_precip:.2f} mm, độ ẩm trung bình {hot_hum:.2f}%")
#         st.write(
#             f"- Tháng lạnh nhất: **{coldest_month[1]}/{coldest_month[0]}** với nhiệt độ trung bình {avg_month_temp[coldest_month]:.2f}°C, lượng mưa trung bình {cold_precip:.2f} mm, độ ẩm trung bình {cold_hum:.2f}%")
#
#         # 4. Chuỗi tháng mùa khô (nóng), mùa mưa (lạnh)
#         st.header("4️⃣ Chuỗi Tháng Nóng (Mùa Khô) và Lạnh (Mùa Mưa)")
#
#         monthly_avg_temp = df.groupby('Month')['Temp_C'].mean()
#         hot_months = monthly_avg_temp[monthly_avg_temp > 28].index.tolist()
#         cold_months = monthly_avg_temp[monthly_avg_temp < 25].index.tolist()
#
#         # Lấy trung bình mưa và ẩm theo tháng nóng/lạnh
#         monthly_avg_precip = df.groupby('Month')['Precipitation_mm'].mean()
#         monthly_avg_hum = df.groupby('Month')['Humidity_pct'].mean()
#
#         st.write(f"- Mùa khô (nóng): các tháng {', '.join(map(str, hot_months))}")
#         for m in hot_months:
#             st.write(
#                 f"  Tháng {m}: Nhiệt độ {monthly_avg_temp[m]:.2f}°C, Lượng mưa {monthly_avg_precip[m]:.2f} mm, Độ ẩm {monthly_avg_hum[m]:.2f}%")
#
#         st.write(f"- Mùa mưa (lạnh): các tháng {', '.join(map(str, cold_months))}")
#         for m in cold_months:
#             st.write(
#                 f"  Tháng {m}: Nhiệt độ {monthly_avg_temp[m]:.2f}°C, Lượng mưa {monthly_avg_precip[m]:.2f} mm, Độ ẩm {monthly_avg_hum[m]:.2f}%")
#
#         # 5. Số ngày nhiệt độ > 35 độ mỗi năm, và ngày mưa lớn > 50 mm
#         st.header("5️⃣ Số Ngày Nóng Cực Đoan ( trên 35°C) và Ngày Mưa Lớn Theo Năm")
#
#         hot_days = df[df['Temp_C'] > 35].groupby('Year').size()
#         heavy_rain_days = df[df['Precipitation_mm'] > 15].groupby('Year').size()
#         combined_days = pd.DataFrame({'HotDays': hot_days, 'HeavyRainDays': heavy_rain_days}).fillna(0).astype(int)
#
#         st.dataframe(combined_days)
#
#         # Vẽ biểu đồ bar dùng plotly
#         def plot_yearly_bar(data, column, title, color_scale, unit):
#             import plotly.graph_objects as go
#             import seaborn as sns
#
#             colors = sns.color_palette(color_scale, len(data)).as_hex()
#             sorted_years = data.sort_values(by=column)['Year'].tolist()
#             color_map = {year: color for year, color in zip(sorted_years, colors)}
#
#             fig = go.Figure()
#             for _, row in data.iterrows():
#                 fig.add_trace(go.Bar(
#                     x=[str(row['Year'])],
#                     y=[row[column]],
#                     text=f"{row[column]} {unit}",
#                     textposition="inside",
#                     marker_color=color_map[row['Year']],
#                     name=str(row['Year']),
#                 ))
#
#             fig.update_layout(
#                 title=title,
#                 xaxis_title="Năm",
#                 yaxis_title=column,
#                 showlegend=False,
#                 height=400
#             )
#             return fig
#
#         combined_days_reset = combined_days.reset_index()
#
#         col1, col2 = st.columns(2)
#
#         with col1:
#             st.plotly_chart(
#                 plot_yearly_bar(combined_days_reset, 'HotDays', "🌡️ Số Ngày > 35°C Theo Năm", 'Reds', "ngày"),
#                 use_container_width=True
#             )
#
#         with col2:
#             st.plotly_chart(
#                 plot_yearly_bar(combined_days_reset, 'HeavyRainDays', "🌧️ Số Ngày Mưa > 50mm Theo Năm", 'Blues',
#                                 "ngày"),
#                 use_container_width=True
#             )
#         # 6. Xu hướng nhiệt độ, lượng mưa, độ ẩm theo năm
#         st.header("6️⃣ Xu Hướng Nhiệt Độ - Lượng Mưa - Độ Ẩm Theo Năm")
#
#         yearly_avg = df.groupby('Year')[['Temp_C', 'Precipitation_mm', 'Humidity_pct']].mean().reset_index()
#         fig, ax = plt.subplots(figsize=(10, 6))
#         sns.regplot(data=yearly_avg, x='Year', y='Temp_C', marker='o', label='Temp_C', ax=ax, color='r')
#         sns.regplot(data=yearly_avg, x='Year', y='Precipitation_mm', marker='x', label='Precipitation_mm', ax=ax,
#                     color='b')
#         sns.regplot(data=yearly_avg, x='Year', y='Humidity_pct', marker='s', label='Humidity_pct', ax=ax, color='g')
#         ax.legend()
#         ax.set_title("Xu hướng Nhiệt Độ, Lượng Mưa và Độ Ẩm theo Năm")
#         st.pyplot(fig)
#
#         # 7. Hiện tượng thời tiết bất thường (nắng nóng kỷ lục, mưa bão lớn)
#         st.header("7️⃣ Hiện Tượng Thời Tiết Bất Thường")
#
#         extreme_temp_days = df[df['Temp_C'] > df['Temp_C'].quantile(0.99)].copy()
#         extreme_rain_days = df[df['Precipitation_mm'] > df['Precipitation_mm'].quantile(0.99)].copy()
#
#         extreme_temp_days['Date'] = extreme_temp_days['Date'].dt.strftime('%Y-%m-%d')
#         extreme_rain_days['Date'] = extreme_rain_days['Date'].dt.strftime('%Y-%m-%d')
#
#         st.subheader("🌞 Ngày Nắng Nóng Kỷ Lục")
#         st.dataframe(extreme_temp_days[['Date', 'Temp_C', 'Precipitation_mm', 'Humidity_pct']])
#
#         st.subheader("🌧️ Ngày Mưa Lớn Bất Thường")
#         st.dataframe(extreme_rain_days[['Date', 'Temp_C', 'Precipitation_mm', 'Humidity_pct']])
#
#         # 8. Heatmap tương quan toàn bộ các biến số (ngoại trừ thời gian)
#         st.header("8️⃣ Biểu Đồ Heatmap Tương Quan Các Biến")
#
#         # Loại bỏ các cột thời gian không cần thiết
#         time_cols = ['Date', 'Year', 'Month', 'Day']
#         corr_data = df.drop(columns=[col for col in time_cols if col in df.columns])
#
#         # Chỉ lấy các cột số để tính tương quan
#         numeric_cols = corr_data.select_dtypes(include=['float64', 'int64']).columns
#
#         corr_matrix = corr_data[numeric_cols].corr()
#
#         # Vẽ heatmap seaborn
#         fig, ax = plt.subplots(figsize=(10, 8))
#         sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='vlag', center=0, square=True, linewidths=0.5, ax=ax)
#         ax.set_title("🌡️💧 Heatmap Tương Quan Các Biến Thời Tiết")
#         st.pyplot(fig)
#
#
#     def show_Visualizations(self):
#         st.header("9️⃣ Visualize Đơn Biến, Nhị Biến")
#
#         df = self.df
#         numeric_cols = ['Temp_C', 'Precipitation_mm', 'Humidity_pct', 'AtmosPressure_hPa']
#
#         # --- Đơn Biến ---
#         st.subheader("🔵 Đơn Biến")
#
#         for col in numeric_cols:
#             st.markdown(f"### {col}")
#
#             # Histogram + KDE (tích hợp trong Plotly histogram)
#             fig = px.histogram(df, x=col, nbins=30, marginal="violin",  # bạn cũng có thể dùng "rug", "box"
#                                title=f" Histogram - KDE: {col}", template="plotly_white")
#             st.plotly_chart(fig, use_container_width=True)
#
#             # Boxplot riêng nếu muốn
#             fig2 = px.box(df, y=col, title=f"Boxplot: {col}", template="plotly_white")
#             st.plotly_chart(fig2, use_container_width=True)
#
#         # --- Nhị Biến ---
#         st.subheader("🟠 Nhị Biến")
#
#         # Scatterplot Temp vs Humidity
#         fig1 = px.scatter(df, x='Temp_C', y='Humidity_pct',
#                           title="Scatter Plot: Nhiệt Độ vs Độ Ẩm",
#                           opacity=0.5, template="plotly_white")
#         st.plotly_chart(fig1, use_container_width=True)
#
#         # Scatterplot Temp vs Pressure
#         fig2 = px.scatter(df, x='Temp_C', y='AtmosPressure_hPa',
#                           title="Scatter Plot: Nhiệt Độ vs Áp Suất",
#                           opacity=0.5, template="plotly_white")
#         st.plotly_chart(fig2, use_container_width=True)
#
#         # Pairplot - Plotly không có trực tiếp nhưng ta có thể dùng `scatter_matrix`
#         st.write("📊 Pairplot (scatterplot matrix) cho các biến numeric (lấy mẫu ngẫu nhiên 500 dòng)")
#         sample_df = df[numeric_cols].sample(500, random_state=42)
#
#         fig3 = px.scatter_matrix(sample_df,
#                                  dimensions=numeric_cols,
#                                  title="Scatter Matrix",
#                                  template="plotly_white",
#                                  height=700)
#         st.plotly_chart(fig3, use_container_width=True)
#
#
# # Sử dụng trong Streamlit app:
# if __name__ == "__main__":
#     st.set_page_config(layout="wide")
#     data = load_data("weather_data_processed.csv")
#     analyzer = WeatherAnalyzer(data)
#     analyzer.show_WeatherStatistics()
#     analyzer.show_Visualizations()

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache_data
def load_data(filepath):
    df = pd.read_csv(filepath)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day

    # Thêm cột mùa: mùa khô, mùa mưa dựa trên tháng
    def season(month):
        if month in [2,3,4,5,6,7,8]:
            return 'Mùa Khô'
        else:
            return 'Mùa Mưa'
    df['Season'] = df['Month'].apply(season)
    return df

class WeatherAnalyzer:
    def __init__(self, df):
        self.df = df

    def filter_data(self, years=None, seasons=None, variables=None):
        df = self.df.copy()
        if years:
            df = df[df['Year'].isin(years)]
        if seasons:
            df = df[df['Season'].isin(seasons)]
        if variables:
            # Chỉ giữ các cột cần thiết, ngoài cột time
            cols = ['Date', 'Year', 'Month', 'Day', 'Season'] + variables
            df = df[cols]
        return df

    def show_filters(self):
        st.sidebar.header("⚙️ Bộ Lọc Tương Tác")
        years = st.sidebar.multiselect(
            "Chọn Năm",
            options=sorted(self.df['Year'].unique()),
            default=sorted(self.df['Year'].unique())
        )
        seasons = st.sidebar.multiselect(
            "Chọn Mùa",
            options=self.df['Season'].unique(),
            default=list(self.df['Season'].unique())
        )
        variables = st.sidebar.multiselect(
            "Chọn Biến Thời Tiết",
            options=['Temp_C', 'Precipitation_mm', 'Humidity_pct', 'AtmosPressure_hPa', 'WindSpeed_kmh', 'CloudCover_pct'],
            default=['Temp_C', 'Precipitation_mm', 'Humidity_pct', 'AtmosPressure_hPa', 'WindSpeed_kmh', 'CloudCover_pct']
        )
        return years, seasons, variables

    def plot_monthly_trends(self, df, variables):
        st.header("📈 Trung Bình Tháng Theo Năm")
        monthly_avg = df.groupby(['Year', 'Month'])[variables].mean().reset_index()

        for var in variables:
            fig = go.Figure()
            years = sorted(monthly_avg['Year'].unique())
            colors = px.colors.qualitative.Dark24

            for i, year in enumerate(years):
                year_data = monthly_avg[monthly_avg['Year'] == year]
                y_vals = [year_data[year_data['Month'] == m][var].values[0] if m in year_data['Month'].values else None for m in range(1,13)]
                fig.add_trace(go.Scatter(
                    x=list(range(1,13)),
                    y=y_vals,
                    mode='lines+markers',
                    name=str(year),
                    line=dict(color=colors[i % len(colors)], width=3),
                    marker=dict(size=7),
                    hovertemplate="Tháng %{x}<br>" + f"{var}: "+"%{y:.2f}<extra></extra>"
                ))

            fig.update_layout(
                title=f"🌡️ {var} Trung Bình Theo Tháng",
                xaxis_title="Tháng",
                yaxis_title=var,
                xaxis=dict(tickmode='linear', dtick=1),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

    def plot_annual_summary(self, df, variables):
        st.header("🗓 Tổng Kết Trung Bình Năm")
        avg_5year = df[variables].mean()
        st.markdown(
            "\n".join([
                f"- **{var} trung bình:** {avg_5year[var]:.2f}" for var in variables
            ])
        )

        monthly_avg_5year = df.groupby('Month')[variables].mean().reset_index()

        for var in variables:
            colors = sns.color_palette("viridis", 12).as_hex()
            sorted_months = monthly_avg_5year.sort_values(by=var)['Month'].tolist()
            color_map = {month: colors[i] for i, month in enumerate(sorted_months)}

            fig = go.Figure()
            for _, row in monthly_avg_5year.iterrows():
                fig.add_trace(go.Bar(
                    x=[row['Month']],
                    y=[row[var]],
                    text=f"{row[var]:.1f}",
                    textposition="inside",
                    marker_color=color_map[row['Month']],
                    name=str(row['Month'])
                ))
            fig.update_layout(
                title=f"{var} Trung Bình Theo Tháng (5 Năm)",
                xaxis_title="Tháng",
                yaxis_title=var,
                showlegend=False,
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

    def plot_extreme_days(self, df):
        st.header("🔥 Ngày Nắng Nóng và Mưa Lớn Bất Thường")
        temp_threshold = df['Temp_C'].quantile(0.99)
        rain_threshold = df['Precipitation_mm'].quantile(0.99)

        extreme_temp_days = df[df['Temp_C'] > temp_threshold].copy()
        extreme_rain_days = df[df['Precipitation_mm'] > rain_threshold].copy()

        extreme_temp_days['Date_str'] = extreme_temp_days['Date'].dt.strftime('%Y-%m-%d')
        extreme_rain_days['Date_str'] = extreme_rain_days['Date'].dt.strftime('%Y-%m-%d')

        st.subheader(f"🌞 Ngày Nhiệt Độ > {temp_threshold:.2f} °C")
        st.dataframe(extreme_temp_days[['Date_str', 'Temp_C', 'Precipitation_mm', 'Humidity_pct']].rename(columns={'Date_str':'Date'}))

        st.subheader(f"🌧️ Ngày Lượng Mưa > {rain_threshold:.2f} mm")
        st.dataframe(extreme_rain_days[['Date_str', 'Temp_C', 'Precipitation_mm', 'Humidity_pct']].rename(columns={'Date_str':'Date'}))

    def plot_correlation_heatmap(self, df, variables):
        st.header("🔗 Heatmap Tương Quan Các Biến")

        corr_matrix = df[variables].corr()

        # Mask tam giác trên
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="vlag", mask=mask, center=0, square=True, linewidths=0.5, ax=ax)
        ax.set_title("Heatmap Tương Quan Các Biến Thời Tiết")
        st.pyplot(fig)

    def plot_scatter_and_hist(self, df, variables):
        st.header("📊 Visualization Đơn và Nhị Biến")
        # Histogram + Boxplot đơn biến
        for var in variables:
            fig = px.histogram(df, x=var, nbins=30, marginal="violin", title=f"Histogram & KDE - {var}")
            st.plotly_chart(fig, use_container_width=True)
            fig_box = px.box(df, y=var, title=f"Boxplot - {var}")
            st.plotly_chart(fig_box, use_container_width=True)

        # Scatter plots cho 2 biến đầu tiên nếu có >= 2 biến
        if len(variables) >= 2:
            for i in range(len(variables)-1):
                fig = px.scatter(df, x=variables[i], y=variables[i+1], opacity=0.5,
                                 title=f"Scatter Plot: {variables[i]} vs {variables[i+1]}")
                st.plotly_chart(fig, use_container_width=True)

    def run(self):
        years, seasons, variables = self.show_filters()
        filtered_df = self.filter_data(years=years, seasons=seasons, variables=variables)

        self.plot_monthly_trends(filtered_df, variables)
        self.plot_annual_summary(filtered_df, variables)
        self.plot_extreme_days(filtered_df)
        self.plot_correlation_heatmap(filtered_df, variables)
        self.plot_scatter_and_hist(filtered_df, variables)


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    data = load_data("weather_data_processed.csv")
    analyzer = WeatherAnalyzer(data)
    analyzer.run()

