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
    def __init__(self, *, passed: bool = False, **kwargs) -> None:
        super().__init__(**kwargs)
        self.passed = passed

    def compose(self) -> ComposeResult:
        yield ResultLabel(passed=self.passed)


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


class TestResultPage(VerticalGroup):
    """TODO"""

    def compose(self) -> ComposeResult:
        """Create test view"""
        yield TestResultBox(passed=True)
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

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header(name=socket.gethostname(), show_clock=True, icon="⚡️")
        yield Footer()
        yield TestResultPage()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = "textual-dark" if self.theme == "textual-light" else "textual-light"


if __name__ == "__main__":
    app = TestViewer()
    app.run()
