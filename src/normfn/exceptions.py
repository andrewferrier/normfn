from typing import override


class FatalError(Exception):
    def __init__(self, value: str) -> None:
        Exception.__init__(self, value)
        self.value: str = value

    @override
    def __str__(self) -> str:
        return repr(self.value)


class QuitError(Exception):
    pass
