import os
import json
import pandas as pd
from .exceptions import OutputConfigError


class OutputHandler():
    """
    Format data and output sheets based on config

    Methods:
        read_config_file() -> None:
            read and parse the config file
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
                "MissingKey": the required keys are missing
        """

        # make sure config file exists
        if not os.path.isfile("configs/" + self.config_filename):
            raise OutputConfigError("ConfigFileNotFound", self.config_filename)

        # read and parse the config
        with open("configs/" + self.config_filename) as config_file:
            try:
                self.config = json.load(config_file)
            except ValueError as error:
                raise OutputConfigError("InvalidSyntax",
                                        self.config_filename, str(error))

        # handle single output file in config
        if type(self.config) is dict:
            self.config = [self.config]

        # make sure the config isn't empty
        if not self.config:
            raise OutputConfigError("MissingOutputFileInfo",
                                    self.config_filename)

        # make sure required keys exist
        missing_keys = []
        for output_file in self.config:
            missing_keys.extend([key for key in ["filename", "sheets"]
                                 if key not in output_file])
            if "sheets" in output_file:
                # handle single sheet in output file
                sheets = ([output_file["sheets"]]
                          if type(output_file["sheets"]) is dict
                          else output_file["sheets"])

                # make sure the sheets aren't empty
                if not sheets:
                    raise OutputConfigError("MissingSheetInfo",
                                            self.config_filename)

                # make sure required keys exist in sheet
                for sheet in sheets:
                    missing_keys.extend([key for key in
                                         ["name", "title", "type", "columns"]
                                         if key not in sheet])
                    if "columns" in sheet:
                        # make sure the columns aren't empty
                        if not (type(sheet["columns"]) is list
                                and sheet["columns"]):
                            raise OutputConfigError("MissingColumnInfo",
                                                    self.config_filename)
                        missing_keys.extend([key for key in
                                             ["from", "name", "type"]
                                             for col in sheet["columns"]
                                             if key not in col])

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

    def format_output_sheet(self,
                            data_df: pd.DataFrame,
                            sheet: any) -> pd.DataFrame:
        """
        Format data into a dataframe for a single sheet based on config

        Arguments:
            data_df (pd.DataFrame):
                dataframe containing data to format
            sheet (object):
                config object of the sheet

        Returns:
            formatted dataframe for a single sheet
        """

        sheet_df = pd.DataFrame()

        for column in sheet["columns"]:
            sheet_df[column["name"]] = data_df[column["from"]]

        return sheet_df

    def generate_output_files(self, data_df: pd.DataFrame) -> None:
        """
        Format data based on config and generate output files

        Arguments:
            data_df (pd.DataFrame):
                dataframe containing data to generate output from
        """

        print(data_df)

        if not os.path.isdir("output_files"):
            os.mkdir("output_files")

        # format data and generate output for each output file
        for output_file in self.config:
            # get path and open file for writing
            output_path = self.generate_output_path(output_file["filename"])
            with pd.ExcelWriter(output_path) as writer:
                # format and save data in a dataframe for each sheet
                for sheet in output_file["sheets"]:

                    sheet_df = self.format_output_sheet(data_df, sheet)
                    sheet_df.to_excel(writer,
                                      sheet_name=sheet["name"],
                                      index=False)
