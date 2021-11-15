import os 
import json

# script_dir = os.path.dirname(__file__)

# with open(os.path.join(script_dir, "test_data.json"), "rt") as fin:
#     new_dict = json.load(fin)

# new_dict = dict()
# sorted(new_dict).reverse

# json_data = json.dumps(new_dict, indent = 5)
# with open(os.path.join(script_dir, "sensor_data.json"), "r+") as fout:
#     fout.write(json_data)

# def write_json(new_data, filename = "sensor_data.json"):
#     with open(filename, "r+") as file:
#         file_data = json.load(file)
#         file_data[""].append(new_data)
#         file.seek(0)
#         json.dump(file_data, file, indent = 4)

# write_json(new_dict)

script_dir = os.path.dirname(__file__)

# TODO: since we are using one RaspPi, this will eventually just take data
# as variables and add it to the current data (it will be much simpler)
with open(os.path.join(script_dir, "test_data.json"), "rt") as fin:
    new_dict = json.load(fin)

with open(os.path.join(script_dir, "sensor_data.json"), "rt") as fout:
    data = json.load(fout)

data.update(new_dict)

with open(os.path.join(script_dir, "sensor_data.json"), "w") as fout:
    json.dump(data, fout)




