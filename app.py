import os
from influxdb_client import InfluxDBClient

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

ORG = "forecasting"
BUCKET = "weather_temperature"
TOKEN = os.getenv("INFLUX_TOKEN")


@st.cache
def get_weather_data(time_range=20):
    """
    Query data and return a Pandas DataFrame
    """
    client = InfluxDBClient(url="http://localhost:8086", token=TOKEN, org=ORG)
    query_api = client.query_api()
    result_df = query_api.query_data_frame(f'from(bucket:"{BUCKET}") '
                                           f'|> range(start: -{time_range}y) '
                                           '|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value") '
                                           '|> keep(columns: ["_time","Measured Fluid", "T (degC)"])')
    result_df['month'] = result_df['_time'].dt.month

    client.close()
    return result_df

print('Getting started...')

chart_df = get_weather_data()

chart_df.rename(columns={"_time": "Date", "T (degC)": "Temperature (°C)"},
                inplace=True)

st.title("Air Temperature (°C) vs. Time")

st.write("## Line Chart")
st.line_chart(chart_df, x="Date", y="Temperature (°C)")

st.write("## Area Chart")
st.area_chart(chart_df, x="Date", y="Temperature (°C)")

chart_month = chart_df.groupby('month')['Temperature (°C)'].mean()

st.write("## Bar Chart\nThis shows the average temperature in each month")

st.bar_chart({'Month number': chart_month.index,
              'Average Temperature (°C)': chart_month.values},
             x="Month number",
             y="Average Temperature (°C)")

