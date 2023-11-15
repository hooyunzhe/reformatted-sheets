import os
import json
import pandas as pd
import numpy as np
from datetime import datetime as dt
from .exceptions import OutputConfigError


class OutputHandler():
    """
    Format data and output sheets based on config

    Methods:
        read_config_file() -> None:
            read and parse the config file
        generate_output_files(data_df: pd.DataFrame) -> None:
            format data based on config and generate output files

    Attributes:
        config (array of objects):
            config objects of the output files
        config_filename (str):
            name of the config file
        current_output_file (object):
            config object of the output file that's being generated
        current_sheet (object):
            config object of the sheet that's being generated
        current_column (object):
            config object of the column that's being formatted
    """

    def __init__(self, config_filename: str) -> None:
        """
        Save the config filename

        Arguments:
            config_filename (str):
                name of the config file
        """

        self.config_filename = config_filename

    def read_config_file(self) -> None:
        """
        Read and parse the config file

        Raises:
            OutputConfigError:
                "ConfigFileNotFound": the file cannot be found
                "InvalidSyntax": the syntax is invalid
                "MissingOutputFileInfo": the output file section is empty
                "MissingSheetInfo": the sheet section is empty
                "MissingColumnInfo": the column section is empty
                "InvalidColumnInfo": the column section contains invalid values
                "MissingKey": the required keys are missing
        """

        # make sure config file exists
        if not os.path.isfile("configs/" + self.config_filename):
            raise OutputConfigError("ConfigFileNotFound", self.config_filename)

        # read and parse config
        with open("configs/" + self.config_filename) as config_file:
            try:
                self.config = json.load(config_file)
            except ValueError as error:
                raise OutputConfigError("InvalidSyntax",
                                        self.config_filename, str(error))

        # handle single output file in config
        if type(self.config) is dict:
            self.config = [self.config]

        # make sure config isn't empty
        if not self.config:
            raise OutputConfigError("MissingOutputFileInfo",
                                    self.config_filename)

        # make sure output files are valid
        missing_keys = []
        for output_file in self.config:
            # make sure required keys exist in output file
            missing_keys.extend([key for key in ["filename", "sheets"]
                                 if key not in output_file])
            if "sheets" in output_file:
                # handle single sheet in output file
                sheets = ([output_file["sheets"]]
                          if type(output_file["sheets"]) is dict
                          else output_file["sheets"])

                # make sure sheets aren't empty
                if not sheets:
                    raise OutputConfigError("MissingSheetInfo",
                                            self.config_filename)

                # make sure sheets are valid
                for sheet in sheets:
                    # make sure required keys exist in sheet
                    missing_keys.extend([key for key in
                                         ["name", "title", "type",
                                          "range", "columns"]
                                         if key not in sheet])
                    if "range" in sheet:
                        # make sure range info isn't empty
                        if not (type(sheet["range"]) is dict
                                and sheet["range"]):
                            raise OutputConfigError("MissingRangeInfo",
                                                    self.config_filename)

                        # make sure range info is valid
                        try:
                            assert "column" in sheet["range"]
                            begin = sheet["range"]["begin"]
                            end = sheet["range"]["end"]
                            begin_dt = dt(begin[0], begin[1], begin[2])
                            end_dt = dt(end[0], end[1], end[2])
                            assert begin_dt <= end_dt
                        except Exception:
                            raise OutputConfigError("InvalidRangeInfo",
                                                    self.config_filename)
                    if "columns" in sheet:
                        # make sure columns aren't empty
                        if not (type(sheet["columns"]) is list
                                and sheet["columns"]):
                            raise OutputConfigError("MissingColumnInfo",
                                                    self.config_filename)

                        # make sure required keys exist in columns
                        for column in sheet["columns"]:
                            if type(column) is dict:
                                if "name" not in column:
                                    missing_keys.append("name")
                                elif ("from" not in column
                                      and "value" not in column):
                                    missing_keys.append("from / value")
                            else:
                                raise OutputConfigError("InvalidColumnInfo",
                                                        self.config_filename)

        # raise exception if there are keys missing
        if missing_keys:
            raise OutputConfigError("MissingKey",
                                    self.config_filename, str(missing_keys))

    def generate_output_path(self, filename: str) -> str:
        """
        Generate full path of the output file based on arguments

        Arguments:
            filename (str):
                name of the output file

        Returns:
            full path of the output file
        """

        return f'output_files/{filename}.xlsx'

    def filter_dataframe(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Filter dataframe to a date range based on config

        Arguments:
            dataframe (pd.DataFrame):
                dataframe containing data to filter

        Returns:
            dataframe filtered to a date range
        """

        # get config object of range
        range_config = self.current_sheet["range"]

        # convert range to timestamps
        range_begin = range_config["begin"]
        range_end = range_config["end"]
        begin_ts = pd.Timestamp(range_begin[0], range_begin[1], range_begin[2])
        end_ts = pd.Timestamp(range_end[0], range_end[1], range_end[2])

        # filter and return dataframe
        return dataframe[(dataframe[range_config["column"]] >= begin_ts)
                         & (dataframe[range_config["column"]] <= end_ts)]

    def format_output_column(self, column_series: pd.Series):
        """
        Format series for a single column in a sheet based on config

        Arguments:
            column_series (pd.Series):
                series containing column to format

        Returns:
            formatted series for a single column
        """

        # handle formatting based on the dtype
        if "format" in self.current_column:
            if np.issubdtype(column_series.dtype, np.datetime64):
                # convert date columns based on format
                return column_series.dt.strftime(
                                        self.current_column["format"])

        return column_series

    def format_output_sheet(self, data_df: pd.DataFrame) -> pd.DataFrame:
        """
        Format data into a dataframe for a single sheet based on config

        Arguments:
            data_df (pd.DataFrame):
                dataframe containing data to format

        Returns:
            formatted dataframe for a single sheet
        """

        # format and save each column of the current sheet
        sheet_df = pd.DataFrame()
        for column in self.current_sheet["columns"]:
            # save config object
            self.current_column = column

            # either take from a column or use a custom value
            if "from" in column:
                sheet_df[column["name"]] = self.format_output_column(
                                                data_df[column["from"]])
            elif "value" in column:
                sheet_df[column["name"]] = column["value"]

        return sheet_df

    def generate_output_files(self, data_df: pd.DataFrame) -> None:
        """
        Format data based on config and generate output files

        Arguments:
            data_df (pd.DataFrame):
                dataframe containing data to generate output from

        Raises:
            OutputConfigError:
                "ColumnNotFound": the specified columns cannot be found
        """

        # print(data_df)

        # make sure the output folder exists
        if not os.path.isdir("output_files"):
            os.mkdir("output_files")

        # format data and generate output for each output file
        for output_file in self.config:
            # save config object
            self.current_output_file = output_file

            # make sure specified columns of each sheet are valid
            for sheet in output_file["sheets"]:
                # make sure specified columns exist in the data
                columns_not_found = [col["from"]
                                     for col in sheet["columns"]
                                     if "from" in col
                                     and col["from"] not in data_df]
                if len(columns_not_found):
                    raise OutputConfigError("ColumnNotFound",
                                            output_file["filename"],
                                            sheet["name"],
                                            str(columns_not_found))

                # make sure specified date column exists and has a date type
                date_col = sheet["range"]["column"]
                if date_col not in data_df:
                    raise OutputConfigError("DateColumnNotFound",
                                            output_file["filename"],
                                            sheet["name"],
                                            date_col)
                if not np.issubdtype(data_df[date_col].dtype, np.datetime64):
                    raise OutputConfigError("InvalidDateColumn",
                                            output_file["filename"],
                                            sheet["name"],
                                            date_col)

            # get path and open file for writing
            output_path = self.generate_output_path(output_file["filename"])
            with pd.ExcelWriter(output_path) as writer:
                # format data and write to output file for each sheet
                for sheet in output_file["sheets"]:
                    # save config object
                    self.current_sheet = sheet

                    # get formatted dataframe
                    sheet_df = self.format_output_sheet(
                                    self.filter_dataframe(data_df))

                    # write to output file
                    sheet_df.to_excel(writer,
                                      sheet_name=sheet["name"],
                                      index=False)
