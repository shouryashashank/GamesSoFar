class Game:
    def __init__(self, id=None, name=None, type=None, platform=None, marketplace=None, source=None, platform_appid=None, source_appid=None, playtime_forever=None, rtime_last_played=None, completed=None, completed_date=None, rating=None, link=None, link2=None, header_image=None, short_description=None, hide=None, createddate=None, metadata=None):
        self.id = id
        self.name = name
        self.type = type
        self.platform = platform
        self.marketplace = marketplace
        self.source = source
        self.platform_appid = platform_appid
        self.source_appid = source_appid
        self.playtime_forever = playtime_forever
        self.rtime_last_played = rtime_last_played
        self.completed = completed
        self.completed_date = completed_date
        self.rating = rating
        self.link = link
        self.link2 = link2
        self.header_image = header_image
        self.short_description = short_description
        self.hide = hide
        self.createddate = createddate
        self.metadata = metadata