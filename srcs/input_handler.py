import os
import json
import pandas as pd

from .exceptions import InputConfigError

class InputHandler():
	"""Parse config and read input files"""

	def __init__(self, config_filename: str) -> None:
		"""Save the config filename"""

		self.config_filename = config_filename


	def read_config_file(self) -> None:
		"""Read and parse the config file

		Raises:
			InputConfigError:
				"FileNotFound": the file cannot be found
				"InvalidConfig": the syntax is invalid
		"""

		# make sure config file exists
		if not os.path.isfile("configs/" + self.config_filename):
			raise InputConfigError("FileNotFound", self.config_filename)

		# read and parse the config
		with open("configs/" + self.config_filename) as config_file:
			try:
				self.config = json.load(config_file)
			except ValueError as error:
				raise InputConfigError("InvalidConfig", self.config_filename, str(error))


	def read_input_files(self) -> pd.DataFrame:
		"""Get data from input files and manipulate based on config

		Returns:
			the dataframe containing data from all input files

		Raises:
			InputConfigError:
				"InputFileNotFound": the input file cannot be found
				"ColumnNotFound": a column cannot be found
				"ColumnsNotFound": more than one column cannot be found
				"InvalidFormat": a column contains data that doesn't match the specified format
		"""

		data = []
		for input_file in self.config:
			# get file path and make sure it exists
			input_path = "input_files/" + input_file["filename"]
			if not os.path.isfile(input_path):
				raise InputConfigError("InputFileNotFound", input_file["filename"])

			# get info of each input file from config
			columns = [col["from"] for col in input_file["columns"]]
			renames = {col["from"]: col["name"] for col in input_file["columns"] if col["from"] != col["name"]}

			# read data from input file
			new_data = pd.read_csv(input_path)

			# make sure specified columns exist and remove the rest
			columns_not_found = [col for col in columns if col not in new_data.columns]
			if len(columns_not_found) == 1:
				raise InputConfigError("ColumnNotFound", input_file["filename"], str(columns_not_found))
			if len(columns_not_found) > 1:
				raise InputConfigError("ColumnsNotFound", input_file["filename"], str(columns_not_found))
			new_data = new_data[columns]

			# rename columns
			new_data.rename(columns = renames, inplace = True)

			# convert date columns based on given format
			for col in input_file["columns"]:
				if col.get("format"):
					try:
						new_data[col["name"]] = pd.to_datetime(new_data[col["name"]], format = col["format"])
					except ValueError as error:
						raise InputConfigError("InvalidFormat", input_file["filename"], col["from"], str(error))

			# add data to array
			data.append(new_data)

		# combine data from all files to one dataframe
		return (pd.concat(data))
