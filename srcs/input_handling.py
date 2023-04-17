import os
import json
import pandas as pd

from srcs import error_handling

def read_config_file(config_filename, error_handler):
	# make sure config file exists
	if not os.path.isfile("configs/" + config_filename):
		error_handler.handle_error("InputConfigFileNotFound")

	# read, parse and return config
	with open("configs/" + config_filename) as config:
		return (json.load(config))

def read_input_files(config_filename, error_handler):
	# set config filename
	error_handler.set_filename(config_filename)

	# read and parse input config
	parsed_config = read_config_file(config_filename, error_handler)

	input_data = []
	for input_file in parsed_config:
		# update current filename
		error_handler.set_filename(input_file["filename"])

		# get file path and make sure it exists
		input_path = "input_files/" + input_file["filename"]
		if not os.path.isfile(input_path):
			error_handler.handle_error("InputFileNotFound")

		# get info of each input file from config
		columns = [col["from"] for col in input_file["columns"]]
		renames = {col["from"]: col["name"] for col in input_file["columns"] if col["from"] != col["name"]}

		# read data
		new_input_data = pd.read_csv(input_path)

		# make sure specified columns exist and remove the rest
		columns_not_found = [col for col in columns if col not in new_input_data.columns]
		if len(columns_not_found) == 1:
			error_handler.handle_error("ColumnNotFound", str(columns_not_found)[1:-1])
		if len(columns_not_found) > 1:
			error_handler.handle_error("ColumnsNotFound", str(columns_not_found))
		new_input_data = new_input_data[columns]

		# rename columns
		new_input_data.rename(columns = renames, inplace = True)

		# convert date columns based on format given
		for col in input_file["columns"]:
			if col.get("format"):
				new_input_data[col["name"]] = pd.to_datetime(new_input_data[col["name"]], format = col["format"])

		# add data to array
		input_data.append(new_input_data)

	# combine data from all files to one dataframe
	return (pd.concat(input_data))