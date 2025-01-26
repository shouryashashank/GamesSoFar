from flet import *
import flet.ads as ads
import json
from steam_web_api import Steam
import datetime

class AddPage(Control):
    def __init__(self, page: Page):
        super().__init__(self)
        self.page = page
        self.user_id_field = TextField(label="User ID")
        self.page.floating_action_button = FloatingActionButton(
                icon=Icons.ARROW_BACK_SHARP,
                data=0,
                on_click=self.go_home,
            )
        self.setup_ui()

    def _get_control_name(self):
        return "container"
    
    def app_bar(self):
        view = AppBar(
            title=Text("Add Page"),
            leading=IconButton(
                icon=Icons.ARROW_BACK_SHARP,
                on_click=self.go_home
            ),
            actions=[
                IconButton(icons.MENU, style=ButtonStyle(padding=0))
            ]
        )
        return view
    def setup_ui(self):
        self.page.add(self.app_bar())
        self.page.add(
            SafeArea(
                content=Column([
                    self.user_id_field,
                    ElevatedButton(text="Go Home", on_click=self.go_home),
                    
                ])
            )
        )
    def go_home(self, e):
        self.page.go('/')
