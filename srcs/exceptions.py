class UsageError(Exception):
	"""When an incorrect number of arguments are passed"""

	def __init__(self, arg_len: int) -> None:
		"""Determine appropriate message based on number of arguments passed

		Args:
			arg_len: The number of arguments
		"""

		# check if there are too little or too many arguments
		message = "not enough arguments" if arg_len < 2 else "too many arguments"

		# send error message and usage info to Exception
		usage = "\nusage: python3 reformatted_sheets.py [input_config] [output_config]"
		super().__init__("UsageError: " + message + usage)


class InputConfigError(Exception):
	"""When an error is found in the input config"""

	def __init__(self, error: str, *args: str) -> None:
		"""Determine appropriate message based on the error

		Args:
			error: The type of the error
			*args: Extra arguments for the message
		"""

		# get the corresponding message and send to Exception
		message = ""

		if error == "FileNotFound":
			message = "file \"" + args[0] + "\" cannot be found in \"configs\" folder"

		if error == "InputFileNotFound":
			message = "input file \"" + args[0] + "\" cannot be found in \"input_files\" folder"

		if error == "ColumnNotFound":
			message = "column " + args[1][1:-1] + " cannot be found in \"" + args[0] + "\""

		if error == "ColumnsNotFound":
			message = "columns " + args[1] + " cannot be found in \"" + args[0] + "\""

		if error == "InvalidConfig":
			message = "file \"" + args[0] + "\" contains invalid syntax"

		if error == "InvalidFormat":
			message = "column '" + args[1] + "' in \"" + args[0] + "\" has "
			message += args[2][:args[2].find("doesn't")] + "which "
			message += args[2][args[2].find("doesn't"):args[2].find('.')]
			message = message.replace(",", "")

		super().__init__("InputConfigError: " + message)
