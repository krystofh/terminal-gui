from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll, VerticalGroup
from textual.widget import Widget
from textual.widgets import Button, Digits, Footer, Header, Collapsible, Label, Static, RichLog
from textual.widgets import DataTable
from textual.reactive import reactive
import socket
import lorem
import time

MOCK_PARAGRAPH = lorem.paragraph() + lorem.paragraph() + lorem.paragraph()


DATA = {
    "status": "ok",
    "count": 42,
    "pi": 3.14159,
    "enabled": True,
    "items": [1, 2, 3],
}


class TopPanel(HorizontalGroup):
    def __init__(self, *, passed: bool = False, serial_number: str = "123", **kwargs) -> None:
        super().__init__(**kwargs)
        self.passed = passed
        self.serial_number = serial_number

    def compose(self) -> ComposeResult:
        yield StateLabel(passed=self.passed)
        yield SerialLabel(serial_number=self.serial_number)
        yield PCBLabel(pcb_id="A7EB")


class StateLabel(Label):
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


class TestResultPanel(VerticalScroll):
    """TODO"""

    def __init__(self, *, passed: bool = False, serial_number: str = "123456", **kwargs) -> None:
        super().__init__(**kwargs)
        self.passed = passed
        self.serial_number = serial_number

    def compose(self) -> ComposeResult:
        """Create test view"""
        yield TopPanel(passed=self.passed, serial_number=self.serial_number)
        with Collapsible(title="Test information"):
            yield DataTable()
        with Collapsible(title="Phase results", collapsed=False):
            yield Static(str(lorem.paragraph()))  # type: ignore
        with Collapsible(title="Errors"):
            yield Static("Errors")
        yield Static(MOCK_PARAGRAPH)


class MainPage(VerticalGroup):
    """
    TODO
    """

    def __init__(self, *, passed: bool = False, serial_number: str = "123456", **kwargs) -> None:
        super().__init__(**kwargs)
        self.passed = passed
        self.serial_number = serial_number

    def compose(self) -> ComposeResult:
        yield TopPanel(passed=self.passed, serial_number=self.serial_number)
        yield ContentPanel()


class ContentPanel(VerticalScroll):
    """
    TODO
    """

    def compose(self) -> ComposeResult:
        yield RichLog(id="log_container", highlight=True, markup=True, max_lines=50)


class TestViewer(App):
    """A Textual app to manage stopwatches."""

    CSS_PATH = "style.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    TITLE = socket.gethostname()

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header(show_clock=True, icon="⚡️")
        yield Footer()
        # yield TestResultPanel(passed=True, serial_number="ABCD123")
        yield MainPage(passed=True, serial_number="ABCD123")

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = "textual-dark" if self.theme == "textual-light" else "textual-light"

    def on_mount(self) -> None:
        self.set_interval(0.1, self._log_tick)

    def _log_tick(self) -> None:
        log = self.query_one("#log_container", RichLog)
        log.write(f"[bold green]INFO[/] example log message @ {time.strftime('%H:%M:%S')}")

    # def on_mount(self) -> None:
    #     table = self.query_one(DataTable)
    #     table.focus()

    #     # Define columns
    #     table.add_columns("Key", "Value")

    #     # Populate from dict
    #     for key, value in DATA.items():
    #         table.add_row(str(key), str(value))

    #     # Optional nice-to-haves
    #     table.cursor_type = "row"
    #     table.zebra_stripes = True


if __name__ == "__main__":
    app = TestViewer()
    app.run()
