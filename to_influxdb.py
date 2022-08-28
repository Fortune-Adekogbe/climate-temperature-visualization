import os
import pandas as pd
import matplotlib.pyplot as plt
from influxdb_client import InfluxDBClient, WriteOptions
from dotenv import load_dotenv

load_dotenv()

df = pd.read_csv("data/jena_climate_2009_2016.csv")[['Date Time', 'T (degC)']]
df.index = pd.to_datetime(df.pop('Date Time'), format='%d.%m.%Y %H:%M:%S')
df['Measured Fluid'] = ['Air'] * df.shape[0]

plt.plot(df['T (degC)'])
# plt.show()

ORG = "forecasting"
BUCKET = "weather_temperature"
TOKEN = os.getenv("INFLUX_TOKEN")

with InfluxDBClient(url="http://localhost:8086", token=TOKEN, org=ORG) as _client:
    with _client.write_api() as _write_client:
        """
        Write Pandas DataFrame
        """
        _write_client.write(BUCKET, ORG, record=df, data_frame_measurement_name='air_temperature',
                            data_frame_tag_columns=['Measured Fluid'])
