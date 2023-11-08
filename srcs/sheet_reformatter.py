from .input_handler import InputHandler
from .output_handler import OutputHandler


class SheetReformatter():
    """
    Transform data into formatted sheets based on configs

    Methods:
        handle_input() -> None:
            read config file and get data from input_handler
        handle_output() -> None:
            read config file and format data into sheets

    Attributes:
        input_handler (InputHandler):
            instance of the InputHandler class
        output_handler (OutputHandler):
            instance of the OutputHandler class
        data (pd.DataFrame):
            data from input files
    """

    def __init__(self, input_config: str, output_config: str) -> None:
        """
        Set up handlers for input and output

        Arguments:
            input_config (str):
                name of the input config file
            output_config (str):
                name of the output config file
        """

        self.input_handler = InputHandler(input_config)
        self.output_handler = OutputHandler(output_config)

    def handle_input(self) -> None:
        """Get data from input_handler"""

        self.input_handler.read_config_file()
        self.data = self.input_handler.read_input_files()

    def handle_output(self) -> None:
        """Format data into sheets"""

        self.output_handler.read_config_file()
