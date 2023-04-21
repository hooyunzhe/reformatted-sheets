import os
import json
import pandas as pd

from .exceptions import OutputConfigError

class OutputHandler():
	"""Format data and output sheets based on config"""

	def __init__(self, config_filename: str) -> None:
		"""Save the config filename"""

		self.config_filename = config_filename


	def read_config_file(self) -> None:
		"""Read and parse the config file

		Raises:
			OutputConfigError:
				"ConfigFileNotFound": the file cannot be found
				"InvalidSyntax": the syntax is invalid
				"MissingOutputFileInfo": the output file section is empty
				"MissingSheetInfo": the sheet section is empty
				"MissingColumnInfo": the column section is empty
				"MissingKey": the required keys are missing
		"""

		# make sure config file exists
		if not os.path.isfile("configs/" + self.config_filename):
			raise OutputConfigError("ConfigFileNotFound", self.config_filename)

		# read and parse the config
		with open("configs/" + self.config_filename) as config_file:
			try:
				self.config = json.load(config_file)
			except ValueError as error:
				raise OutputConfigError("InvalidSyntax", self.config_filename, str(error))

		# handle single output file in config
		if type(self.config) == dict:
			self.config = [self.config]

		# make sure the config isn't empty
		if not self.config:
			raise OutputConfigError("MissingOutputFileInfo", self.config_filename)

		# make sure required keys exist
		missing_keys = []
		for output_file in self.config:
			missing_keys.extend([key for key in ["filename", "sheets"] if key not in output_file])
			if "sheets" in output_file:
				# handle single sheet in output file
				sheets = [output_file["sheets"]] if type(output_file["sheets"]) == dict else output_file["sheets"]

				# make sure the sheets aren't empty
				if not sheets:
					raise OutputConfigError("MissingSheetInfo", self.config_filename)

				# make sure required keys exist in sheet
				for sheet in sheets:
					missing_keys.extend([key for key in ["name", "title", "type", "columns"] if key not in sheet])
					if "columns" in sheet:
						# make sure the columns aren't empty
						if not sheet["columns"] or type(sheet["columns"]) == dict:
							raise OutputConfigError("MissingColumnInfo", self.config_filename)
						missing_keys.extend([key for key in ["from", "name", "type"] for col in sheet["columns"] if key not in col])

		# raise exception if there are keys missing
		if missing_keys:
			raise OutputConfigError("MissingKey", self.config_filename, str(missing_keys))

