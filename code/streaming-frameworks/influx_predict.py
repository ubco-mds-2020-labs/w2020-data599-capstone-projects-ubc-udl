import numpy as np


def extract_data(line):
    """
    Extracts information from InfluxDB line protocol and output as list.

    Keyword arguments:
    line -- input line protocol, string

    Returns:
    data_list -- output of extracted information, list
    """
    split_line = line.split(",")
    split_last = split_line[-1].split()

    find_id = list(map(lambda x: "id=" in x, split_line))
    find_val = list(map(lambda x: "measurement=" in x, split_last))

    id_full = np.array(split_line)[find_id][0]
    val_full = np.array(split_last)[find_val][0]

    id_nolabel = id_full.replace("id=", "")
    val_nolabel = val_full.replace("measurement=", "")
    extract_time = split_last[-1]

    output_dict = {
        "id": id_nolabel,
        "measurement": val_nolabel,
        "timestamp": extract_time,
    }

    return output_dict


def predict_anomaly(data_dict):
    """
    Uses output from `extract_data()` to predict if result is anomalous or not.

    Keyword arguments:
    data_dict -- data to make prediction on, dict

    Returns:
    prediction -- true if anomalous and false if not, boolean
    """

    return data_dict["measurement"] < 10


def convert_data(data_dict, predict_result):
    """
    Converts extracted data and prediction to InfluxDB line protocol.

    Keyword arguments:
    data_dict -- data to make prediction on, dict
    predict_result -- True/False anomaly prediction, boolean

    Returns:
    line_protocol -- data formatted in InfluxDB line protocol, string
    """

    if predict_result:
        anomaly_output = "anomaly=True"
    else:
        anomaly_output = "anomaly=False"

    id_out = "id=" + data_dict["id"]
    val_out = "measurement=" + data_dict["measurement"]

    output = "CHECK_ANOMALY," + " ".join(
        [id_out, val_out, anomaly_output, data_dict["timestamp"]]
    )

    return output
