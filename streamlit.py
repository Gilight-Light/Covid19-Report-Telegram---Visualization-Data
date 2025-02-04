import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import time
from streamlit_extras.metric_cards import style_metric_cards
import plotly.graph_objs as go
from query import query ## Use this when you want query to db
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from joblib import load
import numpy as np




st.set_page_config(
    page_title="CoVid19 Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

#######################
# CSS styling
st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)

alt.themes.enable("dark")

# load data from database
df = query() 

# # load data from csv for streamlit cloud
# file_path = 'data/Clean_Dataset.csv'
# df = pd.read_csv(file_path)
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
df['date'] = pd.to_datetime(df['date'].str.split().str[0], format='%Y-%m-%d')
df['date'] = pd.to_datetime(df['date']).dt.date
unique_dates = df["date"].astype(str).unique()
country_region = df["country_region"].unique()
country_region = np.append(country_region, 'All')
# Lấy dữ liệu tại ngày mới nhất
top = df[df['date'] == df['date'].max()]

# Sử dụng danh sách để chọn các cột cần nhóm
world = top.groupby('country_region')[['confirmed', 'active', 'deaths']].sum().reset_index()

# Hiển thị 5 dòng đầu tiên
print(world.head())


# Sidebar
with st.sidebar:
    st.markdown('<h1 style="color:blue;">🏂 Covid19 Dashboard</h1>', unsafe_allow_html=True)
    # year_list = list(df.date.unique())[::-1]
    
    # selected_year = st.selectbox('Select a year', year_list)
    # df_selected = df[df.airline == selected_year]
    # df_selected_year_sorted = df_selected.sort_values(by="date", ascending=False)
    selected_date_range = st.date_input(
        "Select a date range",
        value=(pd.to_datetime("2020-01-22"), pd.to_datetime("2020-07-27")),
        min_value=df['date'].min(),  # Giới hạn ngày bắt đầu
        max_value=df['date'].max()   # Giới hạn ngày kết thúc
    )
    select_country = st.selectbox('Select a Country_region', country_region, index=len(country_region) - 1)

    if len(selected_date_range) == 2:  # Đảm bảo người dùng đã chọn đủ 2 ngày
        start_date, end_date = selected_date_range
        df_selected = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        df_selected = df_selected.sort_values(by="date", ascending=False)
        if select_country != 'All':
            df_selected = df_selected[df_selected['country_region'] == select_country]
    else:
        st.warning("Please select a valid date range.")


    

st.header("Covid19 Dashboard 🌍🌍🌍")

def Home():
    """
    Display the home page with various analytical metrics and visualizations.
    """
    with st.expander("VIEW EXCEL DATASET"):
        showData = st.multiselect('Filter: ', df_selected.columns.tolist(), default=df_selected.columns.tolist())
        st.dataframe(df_selected[showData], use_container_width=True)

    last_date = df_selected['date'].max()
    df_last_day = df_selected[df_selected['date'] == last_date]
    count_comfirmed = float(df_last_day['confirmed'].sum())  # Sửa lại từ 'active' thành 'confirmed'
    count_dead = float(df_last_day['deaths'].sum())
    count_recovered = float(df_last_day['recovered'].sum())
    count_active = float(df_last_day['active'].sum())  # Đảm bảo có cột 'active' cho số ca đang điều trị
    max_confirmed_country = df.loc[df['confirmed'].idxmax()]
    max_confirmed_country = max_confirmed_country['country_region']
    min_confirmed_country = df.loc[df['confirmed'].idxmin()]

    total1, total2, total3, total4, total5, total6 = st.columns(6, gap='small')
    with total1:
        st.info('Tổng Số Ca Xác Nhận Được Ghi Nhận', icon="💉")
        st.metric(label="Tổng Số Ca Xác Nhận Được Ghi Nhận", value=f"{count_comfirmed:,.0f}")

    with total2:
        st.info('Tổng Số Ca Tử Vong Được Ghi Nhận', icon="⚰️")
        st.metric(label="Tổng Số Ca Tử Vong Được Ghi Nhận", value=f"{count_dead:,.0f}")

    with total3:
        st.info('Tổng Số Ca Phục Hồi Được Ghi Nhận', icon="💚")
        st.metric(label="Tổng Số Ca Phục Hồi Được Ghi Nhận", value=f"{count_recovered:,.0f}")

    with total4:
        st.info('Tổng Số Ca Đang Điều Trị Được Ghi Nhận', icon="💊")
        st.metric(label="Tổng Số Ca Đang Điều Trị Được Ghi Nhận", value=f"{count_active:,.0f}")

    with total5:
        st.info('Quốc Gia Có Số Ca Nhiễm Cao Nhất', icon="🌍")
        st.metric(label="Quốc Gia Có Số Ca Cao Nhất", value=f"{max_confirmed_country}")

    with total6:
        st.info('Quốc Gia Có Số Ca Nhiễm Thấp Nhất', icon="🌏")
        st.metric(label="Quốc Gia Có Số Ca Thấp Nhất", value=f"{min_confirmed_country['country_region']}")

    style_metric_cards(background_color="#FFFFFF", border_left_color="#686664", border_color="#000000", box_shadow="#F71938")


Home()

# death chart
# death chart
fig_deaths = px.scatter_geo(world, 
                     locations="country_region", 
                     locationmode='country names', 
                     color="deaths", 
                     hover_name="country_region", 
                     size="confirmed",  # Sử dụng cột 'confirmed' cho kích thước
                     hover_data=['country_region', 'deaths'],
                     projection="natural earth", 
                     title='Số Ca Tử Vong Tại Mỗi Quốc Gia',
                     color_continuous_scale='Earth',  # Dải màu tự nhiên phù hợp với chủ đề địa cầu
                     labels={'deaths': 'Số Ca Tử Vong'},
                     template="plotly",  # Chủ đề sáng
                     )
fig_deaths.update_geos(showcoastlines=True, coastlinecolor="Black", showland=True, landcolor="lightgray")
fig_deaths.update_layout(
    title=dict(font=dict(size=20, family="Arial", color="black"), x=0.5),  # Tiêu đề màu đen và căn giữa
    margin={"r":0,"t":40,"l":0,"b":0},  # Điều chỉnh lề để tối ưu hóa không gian
    font=dict(color="black")  # Màu chữ là đen để dễ đọc trên nền sáng
)





# confirmed chart
top = df[df['date'] == df['date'].max()]
top_casualities = top.groupby(by = 'country_region')['confirmed'].sum().sort_values(ascending = False).head(20).reset_index()

df1 = df.copy()
df1['date'] = pd.to_datetime(df1['date']).dt.strftime('%m/%d/%Y')
df1 = df1.fillna('-')

    # Tạo biểu đồ với cải tiến
fig = px.density_mapbox(
    df1,
    lat='lat',
    lon='long',
    z='confirmed',
    radius=25,  # Tăng bán kính để làm nổi bật các vùng
    zoom=2,  # Zoom vừa phải để xem chi tiết hơn
    hover_data=["country_region", 'province_state', "confirmed"],  # Thông tin hiển thị khi di chuột
    mapbox_style="open-street-map",  # Đổi nền bản đồ
    animation_frame='date',
    range_color=[0, 15000],  # Mở rộng dải màu
    title='Spread of Covid-19 Over Time',
    color_continuous_scale='Earth',  # Giữ nguyên dải màu 'Earth' như bạn đã chọn
)

# Cập nhật bố cục biểu đồ
fig.update_layout(
    margin={"r": 10, "t": 50, "l": 10, "b": 10},
    title_font=dict(size=24, color='darkblue', family='Arial'),
    coloraxis_colorbar=dict(
        title="Confirmed Cases",
        tickvals=[0, 5000, 10000, 15000],
        ticktext=["Low", "Moderate", "High", "Very High"]
    ),
    width=800,  # Điều chỉnh chiều rộng của bản đồ (có thể điều chỉnh theo kích thước mong muốn)
    height=600,  # Điều chỉnh chiều cao của bản đồ
)

st.plotly_chart(fig, use_container_width=True)

col = st.columns((5,5), gap='medium')
with col[0]:
    plt.figure(figsize=(15, 10))
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.xlabel("Total cases", fontsize=30)
    plt.ylabel('Country', fontsize=30)
    plt.title("Top 20 Quốc Gia Có Số Ca Nhiễm Nhiều Nhất", fontsize=30)
    
    ax = sns.barplot(x=top_casualities.confirmed, y=top_casualities.country_region)
    
    # Thêm giá trị vào từng thanh của biểu đồ
    for i, (value, name) in enumerate(zip(top_casualities.confirmed, top_casualities.country_region)):
        ax.text(value, i - .05, f'{value:,.0f}', size=10, ha='left', va='center')

    # Thiết lập lại nhãn
    ax.set(xlabel='Total cases', ylabel='Country')

    # Hiển thị biểu đồ trong Streamlit
    st.pyplot(plt)
with col[1]:
    st.plotly_chart(fig_deaths, use_container_width=True)

china = df[df.country_region == 'China']
china = china.groupby(by='date')[['recovered', 'deaths', 'confirmed', 'active']].sum().reset_index()
# Nếu date đã là Timestamp, bạn không cần dùng strptime nữa
china['date'] = pd.to_datetime(china['date'])
us = df[df.country_region == 'US']
us = us.groupby(by='date')[['recovered', 'deaths', 'confirmed', 'active']].sum().reset_index()
us = us.iloc[33:].reset_index().drop('index', axis=1)
us['date'] = pd.to_datetime(us['date'])  # Convert date column to datetime
vietnam = df[df.country_region == 'Vietnam']
vietnam = vietnam.groupby(by='date')[['recovered', 'deaths', 'confirmed', 'active']].sum().reset_index()
vietnam = vietnam.iloc[9:].reset_index().drop('index', axis=1)
vietnam['date'] = pd.to_datetime(vietnam['date'])  # Convert date column to datetime
india = df[df.country_region == 'India']
india = india.groupby(by='date')[['recovered', 'deaths', 'confirmed', 'active']].sum().reset_index()
india = india.iloc[8:].reset_index().drop('index', axis=1)
india['date'] = pd.to_datetime(india['date'])  # Convert date column to datetime

df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# Chuyển cột 'date' thành kiểu chuỗi (nếu chưa là chuỗi)
df['date'] = pd.to_datetime(df['date'])

# Lọc dữ liệu cho Hoa Kỳ, Trung Quốc và Ấn Độ
df_us = df[df['country_region'] == 'US']
df_cn = df[df['country_region'] == 'China']
df_in = df[df['country_region'] == 'India']
df_vn = df[df['country_region'] == 'Vietnam']

# Vẽ biểu đồ
plt.figure(figsize=(10, 6))
plt.plot(df_us['date'], df_us['confirmed'], label='Hoa Kỳ', color='blue')
plt.plot(df_cn['date'], df_cn['confirmed'], label='Trung Quốc', color='red')
plt.plot(df_in['date'], df_in['confirmed'], label='Ấn Độ', color='green')
plt.plot(df_vn['date'], df_vn['confirmed'], label='Việt Nam', color='yellow')
# Thêm tiêu đề và nhãn
plt.title('So sánh số ca nhiễm COVID-19 giữa Hoa Kỳ, Trung Quốc, Ấn Độ và Việt Nam')
plt.xlabel('Ngày')
plt.ylabel('Số ca nhiễm')
plt.legend()

# Hiển thị biểu đồ
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(plt)

col = st.columns(2, gap='medium')

# Cột đầu tiên
with col[0]:
    # Tạo biểu đồ cho Việt Nam
    plt.figure(figsize=(10,6))
    sns.pointplot(x=vietnam.date.dt.isocalendar().week, y=vietnam.confirmed)
    plt.title("VietNam's Confirmed Cases Over Time", fontsize=25)
    plt.xlabel('No. of Weeks', fontsize=15)
    plt.ylabel('Total cases', fontsize=15)
    st.pyplot(plt)

# Cột thứ hai
with col[1]:
    # Tạo biểu đồ cho Trung Quốc
    plt.figure(figsize=(10,6))
    sns.pointplot(x=china.date.dt.isocalendar().week, y=china.confirmed)
    plt.title("China's Confirmed Cases Over Time", fontsize=25)
    plt.xlabel('No. of Weeks', fontsize=15)
    plt.ylabel('Total cases', fontsize=15)
    st.pyplot(plt)

# Chia layout thành hai cột cho các biểu đồ còn lại
col = st.columns(2, gap='medium')

# Cột đầu tiên
with col[0]:
    # Tạo biểu đồ cho Mỹ
    plt.figure(figsize=(10,6))
    sns.pointplot(x=us.date.dt.isocalendar().week, y=us.confirmed)
    plt.title("US's Confirmed Cases Over Time", fontsize=25)
    plt.xlabel('No. of Weeks', fontsize=15)
    plt.ylabel('Total cases', fontsize=15)
    st.pyplot(plt)

# Cột thứ hai
with col[1]:
    # Tạo biểu đồ cho Ấn Độ
    plt.figure(figsize=(10,6))
    sns.pointplot(x=india.date.dt.isocalendar().week, y=india.confirmed)
    plt.title("India's Confirmed Cases Over Time", fontsize=25)
    plt.xlabel('No. of Weeks', fontsize=15)
    plt.ylabel('Total cases', fontsize=15)
    st.pyplot(plt)