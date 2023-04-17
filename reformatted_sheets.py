import sys
from srcs import error_handling
from srcs import input_handling

def main(args):
	# set up error handling
	error_handler = error_handling.ErrorHandler("")

	# make sure both configs are provided
	if len(args) != 2:
		error_handler.handle_error("InvalidArguments")

	# read input data
	input_data = input_handling.read_input_files(args[0], error_handler)

	print(input_data)
	print(input_data.dtypes)

# call main if ran directly and not by import
if __name__ == "__main__":
	main(sys.argv[1:])
