import telegraf_inline

while True:
    data = input()
    parsed = telegraf_inline.extract_data(data)
    predict_test = telegraf_inline.predict_anomaly(parsed)
    output = telegraf_inline.convert_data(parsed, predict_test)
    print(output)
