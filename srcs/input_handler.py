import os
import json
import pandas as pd
from .exceptions import InputConfigError


class InputHandler():
    """
    Parse config and read input files

    Methods:
        read_config_file() -> None:
            read and parse the config file
        read_input_files() -> pd.DataFrame:
            get data from input files and manipulate based on config

    Attributes:
        config (array of objects):
            config objects of the input files
        config_filename (str):
            name of the config file

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
            InputConfigError:
                "ConfigFileNotFound": the config file cannot be found
                "InvalidSyntax": the syntax is invalid
                "MissingInputFileInfo": the input file section is empty
                "MissingColumnInfo": the column section is empty
                "MissingKey": the required keys are missing
        """

        # make sure config file exists
        if not os.path.isfile("configs/" + self.config_filename):
            raise InputConfigError("ConfigFileNotFound", self.config_filename)

        # read and parse the config
        with open("configs/" + self.config_filename) as config_file:
            try:
                self.config = json.load(config_file)
            except ValueError as error:
                raise InputConfigError("InvalidSyntax",
                                       self.config_filename, str(error))

        # handle single input file in config
        if type(self.config) is dict:
            self.config = [self.config]

        # make sure the config isn't empty
        if not self.config:
            raise InputConfigError("MissingInputFileInfo",
                                   self.config_filename)

        # make sure required keys exist
        missing_keys = []
        for input_file in self.config:
            missing_keys.extend([key for key in ["filename", "columns"]
                                 if key not in input_file])
            if "columns" in input_file:
                # make sure the columns aren't empty
                if not (type(input_file["columns"]) is list
                        and input_file["columns"]):
                    raise InputConfigError("MissingColumnInfo",
                                           self.config_filename)

                # make sure required keys exist in columns
                missing_keys.extend(["name"
                                    for col in input_file["columns"]
                                    if "name" not in col])
                missing_keys.extend(["from / value"
                                    for col in input_file["columns"]
                                    if "from" not in col
                                    and "value" not in col])

        # raise exception if there are keys missing
        if missing_keys:
            raise InputConfigError("MissingKey",
                                   self.config_filename, str(missing_keys))

    def read_input_files(self) -> pd.DataFrame:
        """
        Get data from input files and manipulate based on config

        Returns:
            dataframe containing data from all input files

        Raises:
            InputConfigError:
                "InputFileNotFound": the input file cannot be found
                "ColumnNotFound": the specified columns cannot be found
                "InvalidFormat": a column contains data that
                                 doesn't match the specified format
                "JoinColumnNotFound": the join_on column cannot be found
                "InvalidJoinColumn": the join_on column
                                     doesn't match any other columns
        """

        # read, manipulate and save data from each input file
        data = []
        join_data = []
        for input_file in self.config:
            # get file path and make sure it exists
            input_path = "input_files/" + input_file["filename"]
            if not os.path.isfile(input_path):
                raise InputConfigError("InputFileNotFound",
                                       input_file["filename"])

            # get info of the columns from config
            columns = []
            new_columns = {}
            renames = {}
            for column in input_file["columns"]:
                # custom name and either column to use or custom value
                if type(column) is dict:
                    if "from" in column:
                        columns.append(column["from"])
                        if column["name"] != column["from"]:
                            renames[column["from"]] = column["name"]
                    elif "value" in column:
                        new_columns[column["name"]] = column["value"]

            # read data from input file
            new_data = pd.read_csv(input_path)

            # make sure specified columns exist and remove the rest
            columns_not_found = [col for col in columns
                                 if col not in new_data.columns]
            if len(columns_not_found):
                raise InputConfigError("ColumnNotFound",
                                       input_file["filename"],
                                       str(columns_not_found))
            new_data = new_data[columns]

            # rename columns
            new_data.rename(columns=renames, inplace=True)

            # convert date columns based on given format
            for col in input_file["columns"]:
                if type(col) is dict and "format" in col:
                    try:
                        new_data[col["name"]] = pd.to_datetime(
                                                new_data[col["name"]],
                                                format=col["format"])
                    except ValueError as error:
                        raise InputConfigError("InvalidFormat",
                                               input_file["filename"],
                                               col["from"], str(error))

            # add new columns with their values
            new_data = new_data.assign(**new_columns)

            # add data to appropriate array
            if "join_on" in input_file:
                # make sure the column exists
                if input_file["join_on"] not in new_data.columns:
                    raise InputConfigError("JoinColumnNotFound",
                                           input_file["filename"],
                                           input_file["join_on"])
                join_data.append((new_data,
                                  input_file["join_on"],
                                  input_file["filename"]))
            else:
                data.append(new_data)

        # combine and join data from all files to one dataframe
        all_data = pd.concat(data)
        for join in join_data:
            if join[1] not in all_data.columns:
                raise InputConfigError("InvalidJoinColumn", join[2], join[1])
            all_data = all_data.merge(join[0], on=join[1], how="left")
        return (all_data)
