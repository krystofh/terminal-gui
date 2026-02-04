from textual.app import App, ComposeResult
from textual.widgets import Footer, Label, Tabs, Static
from textual.containers import VerticalScroll
import lorem

TAB_NAMES = [
    "Logs",
    "Summary",
]

MOCK_PARAGRAPH = ""
for i in range(10):
    MOCK_PARAGRAPH += lorem.paragraph()


# class ContentPanel(VerticalScroll):
#     yield Static()


class TabsApp(App):
    """Demonstrates the Tabs widget."""

    CSS = """
    Tabs {
        dock: top;
    }
    Screen {
        align: center middle;
    }
    Label {
        margin:0 0;
        width: 100%;
        height: 100%;
        background: $panel;
        # border: tall $primary;
        content-align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        yield Tabs(*TAB_NAMES)
        yield Label()
        yield Footer()

    def on_mount(self) -> None:
        """Focus the tabs when the app starts."""
        # self.query_one(Tabs).focus()
        self.query_children(Tabs).focus()

    def update_tab_text(self, label: Label, tab_name: str):
        if tab_name == "Logs":
            label.update(MOCK_PARAGRAPH)
        else:
            label.update("Hello " + tab_name)

    def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
        """Handle TabActivated message sent by Tabs."""
        label = self.query_one(Label)
        if event.tab is None:
            # When the tabs are cleared, event.tab will be None
            label.visible = False
        else:
            label.visible = True
            # label.update("Hello " + event.tab.label)
            self.update_tab_text(label=label, tab_name=event.tab.label)


if __name__ == "__main__":
    app = TabsApp()
    app.run()
