import predict_telegraf_func

while True:
    data = input()
    parsed = predict_telegraf_func.extract_data(data)
    predict_test = predict_telegraf_func.predict_anomaly(parsed)
    output = predict_telegraf_func.convert_data(parsed, predict_test)
    print(output)