# TODO
- Implement `range_begin` and `range_end`
- Implement sheet type `pivot` and column types `column/value`
- Implement title and related formatting
- ~~Create SheetReformatter class~~
- ~~Create OutputHandler class~~

## Config | input
- ~~Handle `columns` as an array of~~
	- ~~short syntax: `"name_of_column"`~~
	- ~~long syntax: `{from, [name], [format]}`~~
- ~~Update exceptions accordingly~~
### Error Handling
- Duplicate columns on input files with `on_join` (maybe) _doesn't break but causes unintended behavior_
- ~~Any missing keywords~~
- ~~Non-existent config file provided~~
- ~~Non-existent file specified in `filename`~~
- ~~Non-existent columns specified in `from`~~
- ~~Invalid formats specified in `format`~~
- ~~Any syntax error~~

## Config | output
- ~~Handle `format` for dates~~
