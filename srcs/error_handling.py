def handle_error(error, arg1 = "", arg2 = ""):
	# get appropriate error message
	message = {
		"InvalidArguments": "usage: python3 reformatted_sheets.py [input_config] [output_config]",
		"InputConfigFileNotFound": "error: input config file \"" + arg1 + "\" cannot be found in \"configs\" folder",
		"InputFileNotFound": "error: input file \"" + arg1 + "\" cannot be found in \"input_files\" folder",
		"ColumnNotFound": "error: column " + arg1 + " cannot be found in " + arg2,
		"ColumnsNotFound": "error: columns " + arg1 + " cannot be found in " + arg2
	}.get(error, "")

	# print error message and exit
	print(message)
	exit(1)
