from dataclasses import (
    asdict,
    dataclass,
)


@dataclass(frozen=True, eq=False)
class ApplicationException(Exception):
    @property
    def meta(self):
        return asdict(self)

    @property
    def message(self):
        return 'An error has occurred in the operation of the application.'
