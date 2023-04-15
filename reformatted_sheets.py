import sys
from srcs import error_handling
from srcs import input_handling

def main(args):
	# make sure both configs are provided
	if len(args) != 2:
		error_handling.handle_error("InvalidArguments")

	# read input data
	input_data = input_handling.read_input_files(args[0])

	print(input_data)
	print(input_data.dtypes)

# call main if ran directly and not by import
if __name__ == "__main__":
	main(sys.argv[1:])
