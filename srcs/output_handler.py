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
				"FileNotFound": the file cannot be found
				"InvalidConfig": the syntax is invalid
		"""

		# make sure config file exists
		if not os.path.isfile("configs/" + self.config_filename):
			raise OutputConfigError("FileNotFound", self.config_filename)

		with open("configs/" + self.config_filename) as config_file:
			try:
				self.config = json.load(config_file)
			except ValueError as error:
				raise OutputConfigError("InvalidConfig", self.config_filename, str(error))
