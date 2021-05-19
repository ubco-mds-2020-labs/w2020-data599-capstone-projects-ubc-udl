import influx_interact
import train_predict

import os

SKYSPARK_Token = os.getenv("SKYSPARK_Token")

# query from InfluxDB
query_client = influx_interact.influx_class(
    org="UBC",
    url="http://206.12.92.81:8086/",
    bucket="SKYSPARK",
    token=SKYSPARK_Token,
)

get_data = query_client.make_query(location="Campus Energy Centre", window=60)
query_client.client.close()

# predict data
predicted_data = train_predict.predict_anomaly_df(get_data)


# write to InfluxDB
write_client = influx_interact.influx_class(
    org="myorg",
    url="http://localhost:8086/",
    bucket="mybucket",
    token="mytoken",
)

write_client.write_data(predicted_data)
write_client.client.close()
