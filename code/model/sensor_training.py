import pandas as pd
import numpy as np
from influx_interact import *
from clean import *

# these to be added with Mitch's PR
# from lstm import *
# from process_results import *

# Define a few variables with the name of your bucket, organization, and token.
bucket = "MDS2021"
org = "UBC"
# UDL provides public users READ access to the InfluxDB 2.0 instance via this token
token = os.environ["SKYSPARK"]
url = "http://206.12.92.81:8086"
