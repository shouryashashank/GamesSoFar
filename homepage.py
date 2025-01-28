from flet import *
import flet.ads as ads
import json
from steam_web_api import Steam
import datetime
from igdb.wrapper import IGDBWrapper
from database import Database



ENABLE_ADS = True

class MainApp(Control):
    def __init__(self, page: Page, steam: Steam):
        super().__init__()
        self.page = page
        self.steam= steam
        self.page.theme.use_material3 = True
        self.game_list = ListView(expand=1, spacing=10, padding=20, auto_scroll=False)  # Initialize game_list as a scrollable Column
        self.user_id_field = TextField(label="User ID")
        self.page.floating_action_button = FloatingActionButton(
                icon=Icons.ADD,
                data=0,
                on_click=self.open_new_page,
            )
        self.setup_ui()
        # Load games when the app starts
        self.load_games(None)
        if ENABLE_ADS and self.page.platform != PagePlatform.WINDOWS:
            self.setup_ads()
    def _get_control_name(self):
        return "container"
    def app_bar(self):
        view = AppBar(
            title=Text("GamesSoFar"),
            actions=[
                IconButton(Icons.MENU, style=ButtonStyle(padding=0))
            ]
        )
        return view
    def setup_ui(self):
        self.page.add(self.app_bar())
        self.page.add(
            SafeArea(
                content=Column([

                    
                    self.user_id_field,
                    ElevatedButton(text="Load Games", on_click=self.reload_games),
                                     
                
                ])
            )
        )
        self.page.add(self.game_list)
        
    
    def open_new_page(self, e):
        self.page.go('/add')

    def reload_games(self, e):
        try:
            user_id = self.user_id_field.value
            # Get user's game list
            games_data = self.get_users_game_list(user_id)
            # Save to JSON
            with open("games.json", "w") as f:
                json.dump(games_data, f)
            self.page.add(Text("Data saved to games.json", color="green"))

            self.load_games(None)
            print("Games reloaded")
        except Exception as ex:
            self.page.add(Text(f"Error: {str(ex)}", color="red"))
            print(f"Error: {str(ex)}")

    def load_games(self, e):
        # with open("games.json", "r", encoding="utf-8") as f:
        #     games_data = json.load(f)
        db = Database()
        db.connect_to_db()
        games_data = db.read_game_db()
        self.game_list.controls.clear()
        for game in games_data:
            for game_id, game_info in game.items():
                header_image = game_info["data"]["header_image"]
                name = game_info["data"]["name"]
                play_time = game_info["data"]["playtime_forever"]
                last_played = datetime.datetime.fromtimestamp(game_info["data"]["rtime_last_played"]).strftime('%Y-%m-%d %H:%M:%S')
                completed = game_info["data"]["completed"]
                short_description = game_info["data"]["short_description"][:100] + "..."  # Truncate description
                website = game_info["data"]["website"]
                list_item = ListTile(
                    leading=Image(src=header_image),
                    title=Text(name),
                    subtitle=Text(f"Playtime: {play_time} minutes \nCompleted: {'Yes' if completed else 'No'} \nLast Played: {last_played}"),
                    on_click=lambda e, link=website: self.page.launch_url(link)
                )
                
                # content=Column([
                #     Image(src=header_image, width=200, height=100),
                #     Text(name, size=20, weight="bold"),
                #     Text(short_description),
                #     Text(f"Playtime: {play_time} minutes"),
                #     Text(f"Last Played: {last_played}"),
                #     Text(f"Completed: {'Yes' if completed else 'No'}")
                    
                # ])
                self.game_list.controls.append(list_item)
        
        self.page.update()


    def save_to_json(self,games_data):
        with open("games.json", "w") as f:
            json.dump(games_data, f)
        self.page.add(Text("Data saved to games.json", color="green"))

    def read_from_json(self, e):
        try:
            with open("user_input.json", "r") as f:
                data = json.load(f)
            self.page.add(Text(f"Read from JSON: {data['user_input']}", color="blue"))
        except FileNotFoundError:
            self.page.add(Text("No data found", color="red"))

    def get_users_game_list(self,user_id):
        user_games = self.steam.users.get_owned_games(user_id)
        game_info = []
        for game in user_games.get("games"):
            try:
                info = self.steam.apps.get_app_details(game["appid"])
                app_id = str(game["appid"])
                fields = [
                ("playtime_forever", 0),
                ("playtime_windows_forever", 0),
                ("playtime_mac_forever", 0),
                ("playtime_linux_forever", 0),
                ("playtime_deck_forever", 0),
                ("rtime_last_played", 0),
                ("completed", False),
                ("completed_date", None),
                ("rating", None)
                ]

                for field, default in fields:
                    info[app_id]["data"][field] = game.get(field, default)
                game_info.append(info)
            except Exception as ex:
                print(f"Error fetching game details for appid {game['appid']} {game}: {str(ex)}")
        return game_info

    def setup_ads(self):
        id_banner = (
            "ca-app-pub-3940256099942544/6300978111"
            if self.page.platform == PagePlatform.ANDROID
            else "ca-app-pub-3940256099942544/2934735716"
        )

        self.page.add(
            Container(
                content=ads.BannerAd(
                    unit_id=id_banner,
                    on_click=lambda e: print("BannerAd clicked"),
                    on_load=lambda e: print("BannerAd loaded"),
                    on_error=lambda e: print("BannerAd error", e.data),
                    on_open=lambda e: print("BannerAd opened"),
                    on_close=lambda e: print("BannerAd closed"),
                    on_impression=lambda e: print("BannerAd impression"),
                    on_will_dismiss=lambda e: print("BannerAd will dismiss"),
                ),
                width=320,
                height=50,
                bgcolor=colors.TRANSPARENT,
                alignment=alignment.bottom_center,
            )
        )
