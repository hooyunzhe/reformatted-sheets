import sys
from srcs import input_handling

def main(args):
    if len(args) != 2:
        print("usage: python3 reformatted_sheets.py [input_config] [output_config]")
        return (1)
    data = input_handling.read_input_files(args[0])
    print(data)
    print(data.dtypes)

if __name__ == "__main__":
    main(sys.argv[1:])
