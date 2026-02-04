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


class ContentPanel(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield Static("Example text", id="content")


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
    #content {
        padding: 1 1;
        width: 100%;
    }
    """

    def compose(self) -> ComposeResult:
        yield Tabs(*TAB_NAMES)
        # yield Label()
        yield ContentPanel()
        yield Footer()

    def on_mount(self) -> None:
        """Focus the tabs when the app starts."""
        # self.query_one(Tabs).focus()
        self.query_children(Tabs).focus()

    def update_tab_text(self, content: Static, tab_name: str):
        if tab_name == "Logs":
            content.update(MOCK_PARAGRAPH)
        else:
            content.update("Hello " + tab_name)

    def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
        """Handle TabActivated message sent by Tabs."""
        content = self.query_one("#content", Static)
        if event.tab is None:
            # When the tabs are cleared, event.tab will be None
            content.visible = False
        else:
            content.visible = True
            # label.update("Hello " + event.tab.label)
            self.update_tab_text(content=content, tab_name=event.tab.label)


if __name__ == "__main__":
    app = TabsApp()
    app.run()
