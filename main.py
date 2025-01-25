from flet import *
import flet.ads as ads
import json

ENABLE_ADS = True

class MainApp:
    def __init__(self, page: Page):
        self.page = page
        self.game_list = Column()  # Initialize game_list here
        # self.text_field = TextField(label="Enter something", color="white")
        # self.save_button = ElevatedButton(text="Save", on_click=self.save_to_json)
        # self.read_button = ElevatedButton(text="Read", on_click=self.read_from_json)
        self.setup_ui()
        # Load games when the app starts
        self.load_games(None)
        if ENABLE_ADS and self.page.platform != PagePlatform.WINDOWS:
            self.setup_ads()

    def setup_ui(self):
        self.page.add(
            SafeArea(
                content=Column([
                    # Text("Hello from Flet", size=30, color="white"),
                    # self.text_field,
                    # self.save_button,
                    # self.read_button
                    self.game_list,
                    ElevatedButton(text="Load Games", on_click=self.load_games)
                
                ])
            )
        )
    def load_games(self, e):
        with open("games.json", "r") as f:
            games_data = json.load(f)
        
        self.game_list.controls.clear()
        for game in games_data:
            for game_id, game_info in game.items():
                header_image = game_info["data"]["header_image"]
                name = game_info["data"]["name"]
                short_description = game_info["data"]["short_description"][:100] + "..."  # Truncate description
                
                game_container = Container(
                    content=Column([
                        Image(src=header_image, width=200, height=100),
                        Text(name, size=20, weight="bold"),
                        Text(short_description)
                    ]),
                    padding=10,
                    border_radius=5,
                    border=BorderSide(1, "black"),
                    margin=5
                )
                self.game_list.controls.append(game_container)
        
        self.page.update()

    def save_to_json(self, e):
        user_input = self.text_field.value
        data = {"user_input": user_input}
        with open("user_input.json", "w") as f:
            json.dump(data, f)
        self.page.add(Text("Data saved to user_input.json", color="green"))

    def read_from_json(self, e):
        try:
            with open("user_input.json", "r") as f:
                data = json.load(f)
            self.page.add(Text(f"Read from JSON: {data['user_input']}", color="blue"))
        except FileNotFoundError:
            self.page.add(Text("No data found", color="red"))

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

def main(page: Page):
    MainApp(page)

app(target=main)