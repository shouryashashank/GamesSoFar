from flet import *
import flet.ads as ads
import json
from steam_web_api import Steam
import datetime
from domain_model.game import Game


class GamePage(Control):
    def __init__(self, page: Page, steam: Steam, game: Game):
        super().__init__(self)
        self.page = page
        self.steam= steam
        self.game = game
        self.page.theme.use_material3 = True
        self.page.floating_action_button = FloatingActionButton(
                icon=Icons.EDIT,
                data=0,
                
            )
        self.setup_ui()

    def _get_control_name(self):
        return "container"
    
    def app_bar(self):
        view = AppBar(
            title=Text(self.game.name),
            leading=IconButton(
                icon=Icons.ARROW_BACK_SHARP,
                on_click=self.go_home
            ),
            actions=[
                IconButton(Icons.MENU, style=ButtonStyle(padding=0))
            ]
        )
        return view
    
    def setup_ui(self):
        self.page.add(self.app_bar())
        
        # Create a container for the image
        image_container = Container(
            content=Image(src=self.game.header_image),
            padding=10
        )
        
        # Create a container for the game details
        details_container = Container(
            content=Column([
                Text(self.game.name, style="headline4"),
                Text(self.game.short_description, style="body1"),
                Text(f"Playtime: {self.game.playtime_forever}", style="body2"),
                Text(f"Last Played: {self.game.rtime_last_played}", style="body2"),
                Text(f"Completed: {self.game.completed}", style="body2"),
                Text(f"Completed Date: {self.game.completed_date}", style="body2"),
                Text(f"Rating: {self.game.rating}", style="body2"),
                Text(f"Link: {self.game.link}", style="body2"),
                Text(f"Link2: {self.game.link2}", style="body2"),
                Text(f"Hide: {self.game.hide}", style="body2"),
                Text(f"Created Date: {self.game.createddate}", style="body2"),
                Text(f"Metadata: {self.game.metadata}", style="body2"),
            ]),
            padding=10
        )
        # Arrange the image and details in a row
        content_row = Row([
            image_container,
            details_container
        ])
        
        safe_area = SafeArea(content=content_row)
        self.page.add(safe_area)

    def go_home(self, e):
        self.page.go('/')
