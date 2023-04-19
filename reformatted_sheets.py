import sys
from srcs.exceptions import UsageError, InputConfigError, OutputConfigError
from srcs.sheet_reformatter import SheetReformatter

def main(args: list[str]) -> None:
	"""Create SheetReformatter instance and call their methods"""

	# make sure both configs are provided
	if len(args) != 2:
		raise UsageError(len(args))

	# initialize with filenames of both configs
	reformatter = SheetReformatter(args[0], args[1])

	# call input handler
	reformatter.handle_input()
	# print(reformatter.data)

	# call output handler
	reformatter.handle_output()


# call main if ran directly and not by import
if __name__ == "__main__":
	# handle exceptions
	try:
		main(sys.argv[1:])
	except (UsageError, InputConfigError, OutputConfigError) as error:
		print(error)
		sys.exit(1)
