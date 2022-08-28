import os
from influxdb_client import InfluxDBClient

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

org = "forecasting"
bucket = "weather_temperature"
TOKEN = os.getenv("INFLUX_TOKEN")


@st.cache
def get_weather_data(time_range=20):
    """
    Query data and return a Pandas DataFrame
    """
    client = InfluxDBClient(url="http://localhost:8086", token=TOKEN, org=org)

    query_api = client.query_api()

    result_df = query_api.query_data_frame(f'from(bucket:"{bucket}") '
                                           f'|> range(start: -{time_range}y) '
                                           '|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value") '
                                           '|> keep(columns: ["_time","Measured Fluid", "T (degC)"])')
    client.close()
    return result_df


print('Getting started...')

chart_df = get_weather_data()

chart_df.rename(columns={"_time": "Date-Time", "T (degC)": "Temperature (°C)"},
                inplace=True)

st.title("Air Temperature (°C) Vs. Time")

chart = st.line_chart(chart_df, x="Date-Time", y="Temperature (°C)")