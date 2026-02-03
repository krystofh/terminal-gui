from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll, VerticalGroup
from textual.widget import Widget
from textual.widgets import Button, Digits, Footer, Header, Collapsible, Label, Static
from textual.reactive import reactive
import socket
import lorem
import time

MOCK_PARAGRAPH = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc sed lacus in "
    "libero dapibus auctor. Morbi at faucibus lorem. Nullam molestie erat velit, quis tempor lacus "
    "lobortis sit amet. Phasellus a magna lacus. Donec molestie vel ipsum non tristique. "
    "Cras commodo nec lorem vitae pharetra. Sed ac ipsum lectus. "
)


class TestResultBox(HorizontalGroup):
    def __init__(self, *, passed: bool = False, serial_number: str = "123", **kwargs) -> None:
        super().__init__(**kwargs)
        self.passed = passed
        self.serial_number = serial_number

    def compose(self) -> ComposeResult:
        yield ResultLabel(passed=self.passed)
        yield SerialLabel(serial_number=self.serial_number)
        yield PCBLabel(pcb_id="A7EB")


class ResultLabel(Label):
    """A Label that displays PASS in green or FAIL in red based on `passed`."""

    passed = reactive(False)

    def __init__(self, *, passed: bool = False, **kwargs) -> None:
        super().__init__("", **kwargs)
        self.passed = passed
        self._update_display()

    def watch_passed(self, passed: bool) -> None:
        self._update_display()

    def _update_display(self) -> None:
        # Remove existing classes before adding new one
        self.remove_class("pass")
        self.remove_class("fail")
        if self.passed:
            self.update("PASS")
            self.add_class("pass")
        else:
            self.update("FAIL")
            self.add_class("fail")


class SerialLabel(Label):
    """Serial number label with same styling as ResultLabel."""

    def __init__(self, *, serial_number: str = "", **kwargs) -> None:
        super().__init__(f"SN: {serial_number}", **kwargs)
        self.add_class("serial")


class PCBLabel(Label):
    """PCB-ID number label with same styling as ResultLabel."""

    def __init__(self, *, pcb_id: str = "", **kwargs) -> None:
        super().__init__(f"PCB-ID: {pcb_id}", **kwargs)
        self.add_class("serial")


class TestResultPage(VerticalGroup):
    """TODO"""

    def __init__(self, *, passed: bool = False, serial_number: str = "123456", **kwargs) -> None:
        super().__init__(**kwargs)
        self.passed = passed
        self.serial_number = serial_number

    def compose(self) -> ComposeResult:
        """Create test view"""
        yield TestResultBox(passed=self.passed, serial_number=self.serial_number)
        with Collapsible(title="Test information"):
            yield Static(MOCK_PARAGRAPH, expand=True)
        with Collapsible(title="Phase results", collapsed=False):
            yield Static(str(lorem.paragraph()))  # type: ignore
        with Collapsible(title="Errors"):
            yield Static("Errors")


class TestViewer(App):
    """A Textual app to manage stopwatches."""

    CSS_PATH = "style.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    TITLE = socket.gethostname()

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header(show_clock=True, icon="⚡️")
        yield Footer()
        yield TestResultPage(passed=True, serial_number="ABCD123")

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = "textual-dark" if self.theme == "textual-light" else "textual-light"


if __name__ == "__main__":
    app = TestViewer()
    app.run()
