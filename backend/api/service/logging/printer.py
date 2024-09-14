from backend.api.service.logging.events import EventTypes
from backend.api.service.assets import shell

PINK = "\033[95m"
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
END_FORMATTING = "\033[0m"


class LogPrinter:
    def __init__(self):
        self.prefix = "|--- "  # |--- Warning: Something is wrong
        # todo: frame the outputs for different kinds of messages

    def print_error(self, error_message: str):
        print(f"{RED}{self.prefix}{error_message}{END_FORMATTING}")

    def print_warning(self, message: str):
        print(f"{YELLOW}{self.prefix}{message}{END_FORMATTING}")

    def print_message(self, message):
        print(f"{CYAN}{self.prefix}{message}{END_FORMATTING}")

    def notify(self, file: str, event_type: str, message: str):
        if event_type == EventTypes.ERROR:
            self.print_error(message)
        elif event_type == EventTypes.WARNING:
            self.print_warning(message)
        elif event_type == EventTypes.MESSAGE:
            self.print_message(message)
