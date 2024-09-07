# This logger aims to follow the Observer Design Pattern.
# Hopefully this turns out good.

class EventTypes:
    # enum class for types of events that can be sent
    WARNING: str
    ERROR: str
    MESSAGE: str


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


class Logger:
    def __init__(self):
        self.observers = []
        self.add_observer(LogPrinter())

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(self, file: str, event_type: str, description: str):
        for observer in self.observers:
            observer.notify(file, event_type, description)

    def message(self, file: str, message: str):
        self.notify_observers(file=file, event_type=EventTypes.MESSAGE, description=message)

    def warning(self, file: str, message: str):
        self.notify_observers(file=file, event_type=EventTypes.WARNING, description=message)

    def exception(self, file: str, exception: Exception):
        message = f"{type(exception).__name__}: {exception}"
        self.notify_observers(file=file, event_type=EventTypes.ERROR, description=message)
