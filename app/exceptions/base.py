from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class ApplicationException(Exception):
    @property
    def message(self):
        return 'An error has occurred in the operation of the application.'
