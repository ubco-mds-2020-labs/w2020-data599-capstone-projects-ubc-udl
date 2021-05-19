import influx_predict

while True:
    data = input()
    parsed = influx_predict.extract_data(data)
    predict_test = influx_predict.predict_anomaly(parsed)
    output = influx_predict.convert_data(parsed, predict_test)
    print(output)
