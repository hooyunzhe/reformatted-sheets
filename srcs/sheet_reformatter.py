from .input_handler import InputHandler
from .output_handler import OutputHandler

class SheetReformatter():
	"""Transform data into formatted sheets based on configs"""

	def __init__(self, input_config: str, output_config: str) -> None:
		"""Set up handlers for input and output"""

		self.input_handler = InputHandler(input_config)
		self.output_handler = OutputHandler(output_config)


	def handle_input(self) -> None:
		"""Get data from input_handler"""

		self.input_handler.read_config_file()
		self.data = self.input_handler.read_input_files()


	def handle_output(self) -> None:
		"""Format data into sheets"""

		self.output_handler.read_config_file()
