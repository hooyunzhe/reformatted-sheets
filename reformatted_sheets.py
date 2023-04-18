import sys
from srcs.exceptions import UsageError, InputConfigError
from srcs.input_handler import InputHandler

def main(args: list[str]) -> None:
	"""Create SheetReformatter instance and call their methods"""

	# make sure both configs are provided
	if len(args) != 2:
		raise UsageError(len(args))

	test = InputHandler(args[0])
	test.read_config_file()

	print(test.read_input_files())


# call main if ran directly and not by import
if __name__ == "__main__":
	# handle exceptions
	try:
		main(sys.argv[1:])
	except (UsageError, InputConfigError) as error:
		print(error)
		sys.exit(1)
