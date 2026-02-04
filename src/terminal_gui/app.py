from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll, VerticalGroup
from textual.widget import Widget
from textual.widgets import (
    Button,
    Digits,
    Footer,
    Header,
    Collapsible,
    Label,
    Static,
    RichLog,
    Tabs,
)
from textual.widgets import DataTable
from textual.reactive import reactive
import socket
import lorem
import time
from states import TestState
from textual.widget import MountError
from textual.css.query import NoMatches

MOCK_PARAGRAPH = ""
for i in range(10):
    MOCK_PARAGRAPH += lorem.paragraph()

MOCK_DATA = {
    "status": "ok",
    "count": 42,
    "pi": 3.14159,
    "enabled": True,
    "items": [1, 2, 3],
}

TAB_NAMES = [
    "Logs",
    "Summary",
]


class TopPanel(HorizontalGroup):
    def __init__(self, *, state: TestState, serial_number: str = "123", **kwargs) -> None:
        super().__init__(**kwargs)
        self.state = state
        self.serial_number = serial_number

    def compose(self) -> ComposeResult:
        yield StateLabel(state=self.state)
        yield SerialLabel(serial_number=self.serial_number)
        yield PCBLabel(pcb_id="A7EB")


class StateLabel(Label):
    """A Label that displays test state with text from enum and corresponding CSS styling."""

    state = reactive(TestState.WAITING)

    def __init__(self, *, state: TestState = TestState.WAITING, **kwargs) -> None:
        super().__init__("", **kwargs)
        self.state = state
        self._update_display()

    def watch_state(self, state: TestState) -> None:
        """Update display based on changed state"""
        self._update_display()

    def _remove_state_attributes(self) -> None:
        """Remove all attributes related to test states"""
        possible_states = list(TestState)
        for state in possible_states:
            self.remove_class(state.class_name())

    def _update_display(self) -> None:
        # Remove existing classes before adding new one
        self._remove_state_attributes()
        # Update the text and attributes
        self.update(str(self.state))
        self.add_class(self.state.class_name())


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

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        """Create test view"""
        with Collapsible(title="Test information", collapsed_symbol="=>", expanded_symbol="^"):
            yield DataTable()
        with Collapsible(
            title="Phase results", collapsed=False, collapsed_symbol="=>", expanded_symbol="^"
        ):
            yield Static(str(lorem.paragraph()))  # type: ignore
        with Collapsible(title="Errors", collapsed_symbol="=>", expanded_symbol="^"):
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
        yield TopPanel(state=TestState.WAITING, serial_number=self.serial_number)
        yield Tabs(*TAB_NAMES)
        yield ContentPanel()


class ContentPanel(VerticalScroll):
    """
    Panel displaying scrollable content of the page, the content of the panel varies between tabs
    """

    def compose(self) -> ComposeResult:
        yield RichLog(id="log_container", highlight=True, markup=True, max_lines=50)
        yield TestResultPanel(id="summary_container")

    def show_logs(self) -> None:
        """Show logs in the content panel"""
        try:
            summary_container = self.get_child_by_id("summary_container")
            summary_container.visible = False
            summary_container.display = False
        except NoMatches:  # container does not exist
            pass
        try:
            log_container = self.get_child_by_id("log_container")
            log_container.visible = True
            log_container.display = True
        except NoMatches:
            pass

    def show_summary(self) -> None:
        """Show test summary in the content panel"""
        try:
            log_container = self.get_child_by_id("log_container")
            log_container.visible = False
            log_container.display = False
        except NoMatches:  # container does not exist
            pass
        try:
            summary_container = self.get_child_by_id("summary_container")
            summary_container.visible = True
            summary_container.display = True
        except NoMatches:
            pass


class TestViewer(App):
    """A Textual app to manage stopwatches."""

    CSS_PATH = "style.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    TITLE = socket.gethostname()
    SUB_TITLE = "PRODUCT"

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header(show_clock=True, icon="⚡️")
        yield Footer()
        yield MainPage(passed=True, serial_number="ABCD123")

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = "textual-dark" if self.theme == "textual-light" else "textual-light"

    def on_mount(self) -> None:
        """Trigger action when App starts"""
        self.set_interval(0.1, self._log_tick)
        # self.query_children(Tabs).focus()
        self.query_one("#summary_container").visible = False
        self.query_one("#summary_container").display = False

    def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
        """Trigger action by clicking tab"""
        if event.tab is None:
            return

        content = self.query_one(ContentPanel)

        if event.tab.label == "Logs":
            content.show_logs()
        elif event.tab.label == "Summary":
            content.show_summary()

    def _log_tick(self) -> None:
        try:
            log = self.query_one("#log_container", RichLog)
            log.write(f"[bold green]INFO[/] example log message @ {time.strftime('%H:%M:%S')}")
        except Exception:
            self.log("Logs unabailable")

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
