import pandas as pd
import matplotlib.pyplot as plt
import os
from influxdb_client import InfluxDBClient, WriteOptions
from dotenv import load_dotenv

load_dotenv()

df = pd.read_csv("data/jena_climate_2009_2016.csv")[['Date Time', 'T (degC)']]
df.index = pd.to_datetime(df.pop('Date Time'), format='%d.%m.%Y %H:%M:%S')
plt.plot(df)
plt.show()
df['Measured Fluid'] = ['Air'] * df.shape[0]
df.to_csv('data/preprocessed.csv')
print(df.head())
print(df.shape)

org = "forecasting"
bucket = "weather_temperature"
token = os.getenv("INFLUX_TOKEN")

with InfluxDBClient(url="http://localhost:8086", token=token, org=org) as _client:

    with _client.write_api(write_options=WriteOptions(batch_size=10000,
                                                      flush_interval=5_000,
                                                      jitter_interval=1_000,
                                                      retry_interval=2_000,
                                                      max_retries=3,
                                                      max_retry_delay=50_000)) as _write_client:
        """
        Write Pandas DataFrame
        """
        _write_client.write(bucket, org, record=df, data_frame_measurement_name='air_temperature',
                            data_frame_tag_columns=['Measured Fluid'])
