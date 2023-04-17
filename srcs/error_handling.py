class ErrorHandler():
	# initial set up
	def __init__(self, filename):
		self.set_filename(filename)

	# the current file with potential errors
	def set_filename(self, filename):
		self.filename = filename

	# if an error is found
	def handle_error(self, error, arg1 = "", arg2 = ""):
		# get appropriate error message
		message = {
			"InvalidArguments": "usage: python3 reformatted_sheets.py [input_config] [output_config]",
			"InputConfigFileNotFound": "error: input config file \"" + self.filename + "\" cannot be found in \"configs\" folder",
			"InputFileNotFound": "error: input file \"" + self.filename + "\" cannot be found in \"input_files\" folder",
			"ColumnNotFound": "error: column " + arg1 + " cannot be found in " + self.filename,
			"ColumnsNotFound": "error: columns " + arg1 + " cannot be found in " + self.filename,
			"InvalidFormat": "error: "
		}.get(error, "")

		# print error message and exit
		print(message)
		exit(1)
