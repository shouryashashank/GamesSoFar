from flet import *
import flet.ads as ads
import json
from steam_web_api import Steam
import datetime
from homepage import MainApp
from addpage import AddPage
from gamepage import GamePage
from domain_model.game import Game
from database import Database

def main(page: Page):
    def route_change(route):
        page.clean()
        KEY = ""
        steam = Steam(KEY)
        if page.route=='/':
            page.add(MainApp(page,steam))
        elif page.route=='/add':
            page.add(AddPage(page,steam))
        elif page.route.startswith('/game/'):
            game_id = int(page.route.split('/')[-1])
            game = get_game_by_id(game_id)  
            page.add(GamePage(page, steam, game))
    def get_game_by_id(game_id):
        db = Database()
        db.connect_to_db()
        game = db.get_game_by_id(game_id)
        db.close_db()
        return game
    if page.theme is None:
        page.theme = Theme()
    page.theme.use_material3 = True
    page.on_route_change = route_change
    page.go('/')

app(target=main)
