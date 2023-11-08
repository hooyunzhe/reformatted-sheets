class UsageError(Exception):
    """When an incorrect number of arguments are passed"""

    def __init__(self, arg_len: int) -> None:
        """
        Determine appropriate message based on number of arguments passed

        Args:
            arg_len: The number of arguments
        """

        # check if there are too little or too many arguments
        message = f"{'not enough' if arg_len < 2 else 'too many'} arguments\n"

        # send error message and usage info to Exception
        padding = "            "
        usage = "python3 reformatted_sheets.py [input_config] [output_config]"
        super().__init__("UsageError: " + message + padding + usage)


class InputConfigError(Exception):
    """When an error is found in the input config"""

    def __init__(self, error: str, *args: str) -> None:
        """
        Determine appropriate message based on the error

        Args:
            error: The type of the error
            *args: Extra arguments for the message
        """

        # get the corresponding message and send to Exception
        message = ""

        if error == "ConfigFileNotFound":
            message = (f'config file "{args[0]}" '
                       'cannot be found in "configs" folder')

        if error == "InvalidSyntax":
            message = (f'config file "{args[0]}" contains invalid syntax\n'
                       f'                  {args[1]}')

        if error == "MissingInputFileInfo":
            message = f'missing input file info in "{args[0]}"'

        if error == "MissingKey":
            message = "missing "
            message += ("keys " + args[1] if "," in args[1]
                        else "key " + args[1][1:-1])
            message += f' in "{args[0]}"'

        if error == "MissingColumnInfo":
            message = f'missing column info in "{args[0]}"'

        if error == "InputFileNotFound":
            message = (f'input file "{args[0]}" '
                       'cannot be found in "input_files" folder')

        if error == "ColumnNotFound":
            message = ("columns " + args[1] if ',' in args[1]
                       else "column " + args[1][1:-1])
            message += f' cannot be found in "{args[0]}"'

        if error == "InvalidFormat":
            message = f"column '{args[1]}' in \"{args[0]}\" has "
            message += args[2][:args[2].find("doesn't")] + "which "
            message += args[2][args[2].find("doesn't"):args[2].find('.')]
            message = message.replace(",", "")

        if error == "JoinColumnNotFound":
            message = (f"'join_on' column '{args[1]}' "
                       f'cannot be found in data from "{args[0]}"')

        if error == "InvalidJoinColumn":
            message = (f"'join_on' column '{args[1]}' from \"{args[0]}\" "
                       "doesn't match any existing columns")

        super().__init__("InputConfigError: " + message)


class OutputConfigError(Exception):
    """When an error is found in the output config"""

    def __init__(self, error: str, *args: str) -> None:
        """
        Determine appropriate message based on the error

        Args:
            error: The type of the error
            *args: Extra arguments for the message
        """

        # get the corresponding message and send to Exception
        message = ""

        if error == "ConfigFileNotFound":
            message = (f'config file "{args[0]}" '
                       'cannot be found in "configs" folder')

        if error == "InvalidSyntax":
            message = (f'config file "{args[0]}" contains invalid syntax\n'
                       f'                   {args[1]}')

        if error == "MissingOutputFileInfo":
            message = f'missing output file info in "{args[0]}"'

        if error == "MissingKey":
            message = "missing "
            message += ("keys " + args[1] if "," in args[1]
                        else "key " + args[1][1:-1])
            message += f' in "{args[0]}"'

        if error == "MissingSheetInfo":
            message = f'missing sheet info in "{args[0]}"'

        if error == "MissingColumnInfo":
            message = f'missing column info in "{args[0]}"'

        if error == "ColumnNotFound":
            message = ("columns " + args[1] if ',' in args[1]
                       else "column " + args[1][1:-1])
            message += f' cannot be found in "{args[0]}"'

        super().__init__("OutputConfigError: " + message)
