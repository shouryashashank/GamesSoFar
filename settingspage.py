from flet import *
import flet.ads as ads
import json
from steam_web_api import Steam
import datetime
from domain_model.game import Game
from domain_model.user import User
from database import Database

class SettingsPage(Control):
    def __init__(self, page: Page, steam: Steam):
        super().__init__(self)
        self.page = page
        self.steam = steam
        self.db = Database()
        self.user = None
        self.page.theme.use_material3 = True
        self.page.floating_action_button = FloatingActionButton(
                icon=Icons.SYNC,
                data=0,
                on_click=self.save_user_data
            )
        self.setup_ui()


    def _get_control_name(self):
        return "container"
    
    def app_bar(self):
        view = AppBar(
            title=Text("Settings"),
            leading=IconButton(
                icon=Icons.ARROW_BACK_SHARP,
                on_click=self.go_home
            ),
            actions=[
                IconButton(Icons.CLOSE, style=ButtonStyle(padding=0),on_click=self.go_home)
            ]
        )
        return view
    
    def setup_ui(self):
        self.page.add(self.app_bar())
        self.load_user_data()
        
    def load_user_data(self):
        self.db.connect_to_db()
        users = self.db.read_user_db()
        self.db.close_db()
        if users:
            self.is_new_user = False
            self.user = users[0]  # Assuming single user for simplicity
            self.name_field = TextField(label="Name", value=self.user.name)
            self.steamid_field = TextField(label="Steam ID", value=self.user.steamid)
            self.googleid_field = TextField(label="Google ID", value=self.user.googleid)
            self.epicid_field = TextField(label="Epic ID", value=self.user.epicid)
            self.gogid_field = TextField(label="GOG ID", value=self.user.gogid)
            self.psid_field = TextField(label="PS ID", value=self.user.psid)
            self.xboxid_field = TextField(label="Xbox ID", value=self.user.xboxid)
            self.nintendoid_field = TextField(label="Nintendo ID", value=self.user.nintendoid)
            self.metadata_field = TextField(label="Metadata", value=self.user.metadata)
        else:
            self.is_new_user = True
            self.user = User()  # Create a new user instance
            self.name_field = TextField(label="Name")
            self.steamid_field = TextField(label="Steam ID")
            self.googleid_field = TextField(label="Google ID")
            self.epicid_field = TextField(label="Epic ID")
            self.gogid_field = TextField(label="GOG ID")
            self.psid_field = TextField(label="PS ID")
            self.xboxid_field = TextField(label="Xbox ID")
            self.nintendoid_field = TextField(label="Nintendo ID")
            self.metadata_field = TextField(label="Metadata")
        
        self.page.add(
            SafeArea(
                content=Column([
                    self.name_field,
                    self.steamid_field,
                    self.googleid_field,
                    self.epicid_field,
                    self.gogid_field,
                    self.psid_field,
                    self.xboxid_field,
                    self.nintendoid_field,
                    self.metadata_field
                ])
            )
        )
        self.page.update()  # Ensure the page is updated after adding components
    
    def save_user_data(self, e):
        if self.user:
            self.user.name = self.name_field.value
            self.user.steamid = self.steamid_field.value
            self.user.googleid = self.googleid_field.value
            self.user.epicid = self.epicid_field.value
            self.user.gogid = self.gogid_field.value
            self.user.psid = self.psid_field.value
            self.user.xboxid = self.xboxid_field.value
            self.user.nintendoid = self.nintendoid_field.value
            self.user.metadata = self.metadata_field.value
            self.db.connect_to_db()
            if self.is_new_user:
                self.user.createddate = datetime.datetime.now()
                self.user.lastupdated = datetime.datetime.now()
                self.db.create_user(self.user)
            else:
                self.user.lastupdated = datetime.datetime.now()
                self.db.update_user(self.user)
            self.db.close_db()
            self.page.snack_bar = SnackBar(Text("User data saved successfully!"))
            self.page.snack_bar.open = True
            self.page.update()

    def go_home(self, e):
        self.page.go('/')
