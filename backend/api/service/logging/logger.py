# This logger aims to follow the Observer Design Pattern.
# Logger sends notifications to every Observer, which handler that event however it wants
# This means that we can simultaneously stream logs to the screen, as well as write to a Text and JSON file.
# Hopefully this turns out good.

from backend.api.service.logging.events import EventTypes
from backend.api.service.logging.printer import LogPrinter


class Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        # This follows the Singleton Design Pattern.
        # We don't want more than one instance of this class anywhere in the code.
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.observers = []
        log_printer = LogPrinter()
        # We only have an observer that prints events on the screen.
        # If we're making this into a proper product, we may need to make this configurable
        self.add_observer(log_printer)

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
