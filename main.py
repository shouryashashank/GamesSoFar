from flet import *
import flet.ads as ads
import json
from steam_web_api import Steam
import datetime
from homepage import MainApp
from addpage import AddPage

def main(page: Page):
    def route_change(route):
        page.clean()
        KEY = ""
        steam = Steam(KEY)
        if page.route=='/':
            page.add(MainApp(page,steam))
        elif page.route=='/add':
            page.add(AddPage(page,steam))
    if page.theme is None:
        page.theme = Theme()
    page.theme.use_material3 = True
    page.on_route_change = route_change
    page.go('/')

app(target=main)
