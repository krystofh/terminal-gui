# States for GUI app

from enum import StrEnum


class TestState(StrEnum):
    """Strings describing state of the test"""

    PASS = "pass"
    FAIL = "fail"
    WAITING = "waiting"
    RUNNING = "running"

    def __str__(self) -> str:
        return self.upper()

    def class_name(self) -> str:
        """Return the class name (from CSS) corresponding to the current state"""
        return self.value
