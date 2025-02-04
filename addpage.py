from flet import *
import flet.ads as ads
import json
from steam_web_api import Steam
import datetime

class AddPage(Control):
    def __init__(self, page: Page, steam: Steam):
        super().__init__(self)
        self.page = page
        self.steam= steam
        self.page.theme.use_material3 = True
        self.user_id_field = TextField(label="Search game")
        self.results_list = ListView(expand=1, spacing=10, padding=20, auto_scroll=False)  # Initialize game_list as a scrollable Column

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
            title=Text("Add Game"),
            leading=IconButton(
                icon=Icons.ARROW_BACK_SHARP,
                on_click=self.go_home
            ),
            actions=[
                IconButton(Icons.MENU, style=ButtonStyle(padding=0), on_click=self.open_settings_page)  # Add on_click event
            ]
        )
        return view
    
    def open_settings_page(self, e):
        self.page.go('/settings')
        
    def setup_ui(self):
        self.page.add(self.app_bar())
        self.page.add(
            SafeArea(
                content=Column([
                    self.user_id_field,
                    ElevatedButton(text="Search", on_click=self.search_game),
                    
                ])
            )
        )
        self.page.add(self.results_list)
    def go_home(self, e):
        self.page.go('/')

    def search_game(self, e):
        search = self.steam.apps.search_games(self.user_id_field.value)
        self.display_results(search['apps'])

    def display_results(self, apps):
        self.results_list.controls.clear()
        for app in apps:
            self.results_list.controls.append(
                ListTile(
                    leading=Image(src=app['img']),
                    title=Text(app['name']),
                    subtitle=Text(app['price']),
                    on_click=lambda e, link=app['link']: self.page.launch_url(link)
                )
            )
        self.page.update()
        
    
