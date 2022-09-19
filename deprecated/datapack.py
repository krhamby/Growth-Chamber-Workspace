import os 
import json

class Data:
    def __init__(self, timestamp, humidity, lux, temperature):
        self.timestamp = timestamp
        self.humidity = humidity
        self.lux = lux
        self.temperature = temperature

script_dir = os.path.dirname(__file__)

# The following code reads the current data and so
# the server can access the correct information
with open(os.path.join(script_dir, "sensor_data.json"), "rt") as fin:
    data_dict = json.load(fin)

data_db = dict()
sorted(data_db).reverse
for d in data_dict.values():
    data_db[d["timestamp"]] = Data(d["timestamp"], d["humidity"], d["lux"], d["temperature"])