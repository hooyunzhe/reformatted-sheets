import json
import pandas as pd

def read_input_files(config_filename):
    with open("configs/" + config_filename) as config:
        parsed_config = json.load(config)

    input_data = []

    for input_file in parsed_config:
        input_path = "input_files/" + input_file["filename"]
        columns = [col["from"] for col in input_file["columns"]]
        new_input_data = pd.read_csv(input_path, usecols = columns)

        renames = {col["from"]: col["name"] for col in input_file["columns"] if col["from"] != col["name"]}
        new_input_data.rename(columns = renames, inplace = True)

        for col in input_file["columns"]:
            if col.get("format"):
                new_input_data[col["name"]] = pd.to_datetime(new_input_data[col["name"]], format = col["format"])

        input_data.append(new_input_data)
    return (pd.concat(input_data))
