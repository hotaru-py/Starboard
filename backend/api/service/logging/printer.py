from backend.api.service.logging.events import EventTypes


class LogPrinter:
    def __init__(self):
        self.prefix = "|--- "  # |--- Warning: Something is wrong
        # todo: frame the outputs for different kinds of messages

    def print_error(self, error_message: str):
        print(error_message)

    def print_warning(self, message: str):
        print(message)

    def print_message(self, message):
        print(message)

    def notify(self, file: str, event_type: str, message: str):
        if event_type == EventTypes.ERROR:
            self.print_error(message)
        elif event_type == EventTypes.WARNING:
            self.print_warning(message)
        elif event_type == EventTypes.MESSAGE:
            self.print_message(message)
