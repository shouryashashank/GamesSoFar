from domain_model.game import Game
import datetime
def steam_to_game(steam_json):
    game = Game(
        name=steam_json.get("name"),
        type=steam_json.get("type"),
        platform="PC",
        source="Steam",
        source_appid=steam_json.get("steam_appid"),
        playtime_forever=steam_json.get("playtime_forever"),
        rtime_last_played=steam_json.get("rtime_last_played"),
        completed=steam_json.get("completed"),
        completed_date=steam_json.get("completed_date"),
        rating=steam_json.get("rating"),
        header_image=steam_json.get("header_image"),
        short_description=steam_json.get("short_description"),
        metadata=steam_json,
        createddate= datetime.datetime.now().isoformat()
    )
    return game