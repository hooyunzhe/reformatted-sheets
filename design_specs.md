# reformatted-sheets

## Usage
- `python3 reformatted_sheets.py [input_config] [output_config]`
- looks for config files in `configs`

## Config | input
- specifies filenames of input files
	- looks for input files in `input_files`
- designates column types

### Syntax
- `array of`
	- `"filename": name of input file`
	- `"columns": array of`
		- `"from": column to use`
		- `"name": name of column`
		- `"format": format of column`
			- `applicable for date|phone`

## Config | output
- specifies filenames of output files
	- saves output files in `output_files`
- configures info and format of output files

### Syntax
- `array of`
	- `"filename": name of output file`
	- `"sheets": array of`
		- `"name": name of sheet`
		- `"title": title of sheet`
		- `"type": type of sheet`
			- `"sheet": columns of type column`
			- `"pivot": columns of types column and value`
		- `"range_begin": date to begin in sheet`
			- `[[year], [month], [day]]`
		- `"range_end": date to end in sheet`
			- `[[year], [month], [day]]`
		- `"columns": array of`
			- `"from": column to use`
			- `"name": name of column`
			- `"type": type of column`
				- `column|value`
			- `"format": format of column`
				- `number-word|string-title|date-month|phone-full"`

