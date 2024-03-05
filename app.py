import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import plotly.express as px
import streamlit as st

# load dataset
df = pd.read_csv("cleaned_dataset.csv")
df['dteday'] = pd.to_datetime(df['dteday'])

st.set_page_config(page_title="Project Dicoding",
                   page_icon="bar_chart:",
                   layout="wide")
#css file
with open('style.css')as f:
 st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)


def create_monthly_users_df(df):
    monthly_users_df = df.resample(rule='M', on='dteday').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    monthly_users_df.index = monthly_users_df.index.strftime('%b-%y')
    monthly_users_df = monthly_users_df.reset_index()
    monthly_users_df.rename(columns={
        "dteday": "yearmonth",
        "cnt": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    return monthly_users_df

def create_seasonly_users_df(df):
    seasonly_users_df = df.groupby("season").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    seasonly_users_df = seasonly_users_df.reset_index()
    seasonly_users_df.rename(columns={
        "cnt": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    seasonly_users_df = pd.melt(seasonly_users_df,
                                      id_vars=['season'],
                                      value_vars=['casual_rides', 'registered_rides'],
                                      var_name='type_of_rides',
                                      value_name='count_rides')
    
    seasonly_users_df['season'] = pd.Categorical(seasonly_users_df['season'],
                                             categories=['Spring', 'Summer', 'Fall', 'Winter'])
    
    seasonly_users_df = seasonly_users_df.sort_values('season')
    
    return seasonly_users_df

def create_weekday_users_df(df):
    weekday_users_df = df.groupby("weekday").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    weekday_users_df = weekday_users_df.reset_index()
    weekday_users_df.rename(columns={
        "cnt": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)

    weekday_users_df = pd.melt(weekday_users_df,
                                      id_vars=['weekday'],
                                      value_vars=['casual_rides', 'registered_rides'],
                                      var_name='type_of_rides',
                                      value_name='count_rides')
    
    weekday_users_df['weekday'] = pd.Categorical(weekday_users_df['weekday'],
                                             categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    
    weekday_users_df = weekday_users_df.sort_values('weekday')
    
    return weekday_users_df

def create_hourly_users_df(df):
    hourly_users_df = df.groupby("hr").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    hourly_users_df = hourly_users_df.reset_index()
    hourly_users_df.rename(columns={
        "cnt": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    return hourly_users_df

# make filter components (komponen filter)

min_date = df["dteday"].min()
max_date = df["dteday"].max()

# ----- SIDEBAR -----

with st.sidebar:
    # add capital bikeshare logo
    st.image("logo.png")

    st.sidebar.header("Filter:")

    # Menampilkan slider untuk memilih rentang tanggal
    start_date = st.sidebar.date_input(
        label="Start Date",
        min_value=min_date,
        max_value=max_date,
        value=min_date
    )

    end_date = st.sidebar.date_input(
        label="End Date",
        min_value=min_date,
        max_value=max_date,
        value=max_date
    )

# hubungkan filter dengan main_df

main_df = df[
    (df["dteday"] >= str(start_date)) &
    (df["dteday"] <= str(end_date))
]

# assign main_df ke helper functions yang telah dibuat sebelumnya

monthly_users_df = create_monthly_users_df(main_df)
weekday_users_df = create_weekday_users_df(main_df)
seasonly_users_df = create_seasonly_users_df(main_df)
hourly_users_df = create_hourly_users_df(main_df)

# ----- MAINPAGE -----
st.title("Bike Sharing Dashboard")
st.markdown("##")

col1, col2, col3 = st.columns(3)

with col1:
    total_all_rides = main_df['cnt'].sum()
    st.metric("Total Rides", value=total_all_rides)
with col2:
    total_casual_rides = main_df['casual'].sum()
    st.metric("Total Casual Rides", value=total_casual_rides)
with col3:
    total_registered_rides = main_df['registered'].sum()
    st.metric("Total Registered Rides", value=total_registered_rides)

st.markdown("---")

# ----- CHART -----
# Membuat dua pilihan plot
plot_options = ['Daily Bikeshare User Count', 'Monthly Bikeshare Usage']
plot_choice = st.radio('Choose Plot Type', plot_options)

# Jika pengguna memilih plot Altair
if plot_choice == 'Daily Bikeshare User Count':
    # Membuat plot dengan Altair
    st.write('Count by bikeshare users by day')

    # Membuat plot menggunakan Altair
    line_chart = alt.Chart(df).mark_line(
        color='darkblue',  # Warna garis
        interpolate='basis'  # Menggunakan kurva yang lebih halus
    ).encode(
        x='dteday:T',
        y='cnt:Q',
        tooltip=['dteday:T', 'cnt:Q']
    )

    area_chart = alt.Chart(df).mark_area(
        color=alt.Gradient(
            gradient='linear',
            stops=[
                alt.GradientStop(color='lightblue', offset=0),  # Warna awal
                alt.GradientStop(color='darkblue', offset=1)   # Warna akhir
            ],
            x1=0,
            x2=1,
            y1=1,
            y2=0
        ),
        line={'color': 'darkblue'},  # Warna garis tepi
        interpolate='basis'  # Menggunakan kurva yang lebih halus
    ).encode(
        x='dteday:T',
        y='cnt:Q',
    )

    # Menggabungkan line chart dan area chart
    chart = alt.layer(area_chart, line_chart).resolve_scale(y='independent')

    # Menampilkan plot menggunakan st.altair_chart
    st.altair_chart(chart, use_container_width=True)

# Jika pengguna memilih plot Plotly
elif plot_choice == 'Monthly Bikeshare Usage':
    # Membuat plot dengan Plotly
    fig = px.line(monthly_users_df,
                  x='yearmonth',
                  y=['casual_rides', 'registered_rides', 'total_rides'],
                  color_discrete_sequence=["#2CA02C", "#FF7F0E", "#1F77B4"],  # Mengatur warna secara manual
                  markers=True,
                  title="Monthly Count of Bike-share Rides")

    # Menyesuaikan tata letak
    fig.update_layout(
        xaxis_title='',  # Menghapus label sumbu X
        yaxis_title='Total Rides',  # Menambahkan label sumbu Y
        font=dict(
            family="Arial",
            size=12,
            color="black"
        ),
        title_font_family="Arial",  # Menyesuaikan font judul
        title_font_size=20,  # Menyesuaikan ukuran font judul
        title_font_color="white"  # Menyesuaikan warna font judul
    )

    # Menampilkan chart menggunakan st.plotly_chart
    st.plotly_chart(fig, use_container_width=True)
# Membuat plot 1
fig1 = px.bar(seasonly_users_df,
              x='season',
              y=['count_rides'],
              color='type_of_rides',
              color_discrete_sequence=["#1f77b4", "#ff7f0e", "#aec7e8"],  # Warna berbeda dari sebelumnya
              title='Count of bike-share rides by season')

# Menyesuaikan tata letak plot 1
fig1.update_layout(
    xaxis_title='',  # Menghapus label sumbu X
    yaxis_title='Total Rides',  # Menambahkan label sumbu Y
    font=dict(
        family="Arial",
        size=12,
        color="white"
    ),
    title_font_family="Arial",  # Menyesuaikan font judul
    title_font_size=20,  # Menyesuaikan ukuran font judul
    title_font_color="white"  # Menyesuaikan warna font judul
)

# Membuat plot 2
fig2 = px.bar(weekday_users_df,
              x='weekday',
              y=['count_rides'],
              color='type_of_rides',
              barmode='group',
              color_discrete_sequence=["#2ca02c", "#98df8a", "#d62728"],  # Warna berbeda dari sebelumnya
              title='Count of bike-share rides by weekday')

# Menyesuaikan tata letak plot 2
fig2.update_layout(
    xaxis_title='',  # Menghapus label sumbu X
    yaxis_title='Total Rides',  # Menambahkan label sumbu Y
    font=dict(
        family="Arial",
        size=12,
        color="white"
    ),
    title_font_family="Arial",  # Menyesuaikan font judul
    title_font_size=20,  # Menyesuaikan ukuran font judul
    title_font_color="white"  # Menyesuaikan warna font judul
)

# Menampilkan plot menggunakan st.plotly_chart
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig1, use_container_width=True)
right_column.plotly_chart(fig2, use_container_width=True)
fig = px.line(hourly_users_df,
              x='hr',
              y=['casual_rides', 'registered_rides'],
              color_discrete_sequence=["skyblue", "orange"],
              markers=True,
              title='Count of bike-share rides by hour of day').update_layout(xaxis_title='', yaxis_title='Total Rides')

st.plotly_chart(fig, use_container_width=True)


# Menampilkan plot 4 dengan Altair
st.write('Clusters of bike-share rides count by season and temperature')

# Membuat plot menggunakan Altair
scatter = alt.Chart(df).mark_circle(size=60).encode(
    x='temp',
    y='cnt',
    color='season',
    tooltip=['temp', 'cnt', 'season']
).properties(
    width=600,
    height=400
).interactive()

# Menampilkan plot menggunakan st.altair_chart
st.altair_chart(scatter, use_container_width=True)





st.caption('Copyright (c), created by Muhammad Farid')

# ----- HIDE STREAMLIT STYLE -----
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)
