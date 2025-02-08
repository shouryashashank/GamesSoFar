from pathlib import Path
import sqlite3 as sqlite
import flet as ft
from datetime import datetime
from domain_model.user import User
from domain_model.game import Game
from typing import List
import json

class Database:
    def __init__(self):
        self.db = None

    def connect_to_db(self):
        try:
            db_path = Path(__file__).parent.parent.joinpath("game.db")
           
            self.db_path = db_path
            self.db = sqlite.connect(db_path)
            c = self.db.cursor()
            c.execute(
                """CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, 
								  name VARCHAR(100) NOT NULL, 
								  createddate DATETIME NOT NULL, 
                                  lastupdated DATETIME NOT NULL, 
								  steamid VARCHAR(50),
								  googleid VARCHAR(255),
								  epicid VARCHAR(255),
								  gogid VARCHAR(255),
								  psid VARCHAR(255), 
								  xboxid VARCHAR(255), 
								  nintendoid VARCHAR(255), 
								  metadata VARCHAR(255))""")
            
            c.execute(
                """CREATE TABLE IF NOT EXISTS games (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                  name VARCHAR(255) NOT NULL UNIQUE,
                                  type VARCHAR(255),
                                  platform VARCHAR(255),
                                  marketplace VARCHAR(255),
                                  source INT,
                                  platform_appid VARCHAR(255),
                                  source_appid VARCHAR(255),
                                  playtime_forever BIGINT,
                                  rtime_last_played DATETIME,
                                  completed BOOLEAN,
                                  completed_date DATETIME,
                                  rating INT,
                                  link VARCHAR(255),
                                  link2 VARCHAR(255),
                                  header_image VARCHAR(255),
                                  short_description VARCHAR(255),
                                  hide BOOLEAN,
                                  createddate DATETIME NOT NULL,
                                  metadata VARCHAR(255))""")
            
            print("Database connected and table ensured.")
            
        except sqlite.DatabaseError as e:
            print("Error: Database not found")
            print(e)
    
    # crud op on user
    def return_db_path(self):
        return self.db_path
    def read_user_db(self):
        """ Read user data from database """
        c = self.db.cursor()
        c.execute("SELECT * FROM users")
        rows = c.fetchall()
        
        users = []
        for row in rows:
            user = User(id=row[0], name=row[1], createddate=row[2], lastupdated=row[3], steamid=row[4], googleid=row[5], epicid=row[6], gogid=row[7], psid=row[8], xboxid=row[9], nintendoid=row[10], metadata=row[11])
            users.append(user)
        
        return users
    
    def create_user(self, user):
        """ Create a new user """
        c = self.db.cursor()
        c.execute("INSERT INTO users (name, createddate, lastupdated, steamid, googleid, epicid, gogid, psid, xboxid, nintendoid, metadata) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (user.name, user.createddate, datetime.now(), user.steamid, user.googleid, user.epicid, user.gogid, user.psid, user.xboxid, user.nintendoid, user.metadata))
        self.db.commit()
        return c.lastrowid
    
    def update_user(self, user):
        """ Update an existing user """
        c = self.db.cursor()
        c.execute("UPDATE users SET name = ?, steamid = ?, googleid = ?, epicid = ?, gogid = ?, psid = ?, xboxid = ?, nintendoid = ?, metadata = ?, lastupdated = ? WHERE id = ?",
                (user.name, user.steamid, user.googleid, user.epicid, user.gogid, user.psid, user.xboxid, user.nintendoid, user.metadata, datetime.now(), user.id))
        self.db.commit()
    
    # crud op on game
    def read_game_db(self, filters=None, sort_by=None, limit=None) -> List[Game]:
        """
        Read game data from database with optional filters, sorting, and limit.
        
        :param filters: Dictionary of column-value pairs to filter the results.
        :param sort_by: Column name to sort the results by.
        :param limit: Maximum number of results to return.
        :return: List of Game objects matching the query.
        """
        query = "SELECT * FROM games"
        params = []

        # Apply filters
        if filters:
            filter_clauses = []
            for column, value in filters.items():
                filter_clauses.append(f"{column} = ?")
                params.append(value)
            query += " WHERE " + " AND ".join(filter_clauses)

        # Apply sorting
        if sort_by:
            query += f" ORDER BY {sort_by}"

        # Apply limit
        if limit:
            query += f" LIMIT {limit}"

        c = self.db.cursor()
        c.execute(query, params)
        rows = c.fetchall()

        games = []
        for row in rows:
            game = Game(
                id=row[0],
                name=row[1],
                type=row[2],
                platform=row[3],
                marketplace=row[4],
                source=row[5],
                platform_appid=row[6],
                source_appid=row[7],
                playtime_forever=row[8],
                rtime_last_played=row[9],
                completed=row[10],
                completed_date=row[11],
                rating=row[12],
                link=row[13],
                link2=row[14],
                header_image=row[15],
                short_description=row[16],
                hide=row[17],
                createddate=row[18],
                metadata=row[19]
            )
            games.append(game)

        return games
    
    def get_game_by_id(self, game_id) -> Game:
        """ Get a game by its ID """
        c = self.db.cursor()
        c.execute("SELECT * FROM games WHERE id = ?", (game_id,))
        row = c.fetchone()
        if row:
            game = Game(
                id=row[0],
                name=row[1],
                type=row[2],
                platform=row[3],
                marketplace=row[4],
                source=row[5],
                platform_appid=row[6],
                source_appid=row[7],
                playtime_forever=row[8],
                rtime_last_played=row[9],
                completed=row[10],
                completed_date=row[11],
                rating=row[12],
                link=row[13],
                link2=row[14],
                header_image=row[15],
                short_description=row[16],
                hide=row[17],
                createddate=row[18],
                metadata=row[19]
            )
            return game
        return None

    def insert_multiple_games(self, games):
        """
        Insert multiple games into the games table.
        
        :param games: List of Game objects.
        """
        try:
            c = self.db.cursor()
            game_tuples = [
                (
                    game.name, game.type, game.platform, game.marketplace, game.source, game.platform_appid, 
                    game.source_appid, game.playtime_forever, game.rtime_last_played, game.completed, 
                    game.completed_date, game.rating, game.link, game.link2, game.header_image, 
                    game.short_description, game.hide, game.createddate, json.dumps(game.metadata)
                )
                for game in games
            ]
            c.executemany(
                """INSERT INTO games (name, type, platform, marketplace, source, platform_appid, source_appid, playtime_forever, 
                                    rtime_last_played, completed, completed_date, rating, link, link2, header_image, 
                                    short_description, hide, createddate, metadata) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                game_tuples
            )
            self.db.commit()
            print("Multiple games inserted successfully.")
        except sqlite.DatabaseError as e:
            print("Error: Failed to insert multiple games")
            print(e)

    def update_game(self, game):
        """ Update an existing game """
        c = self.db.cursor()
        c.execute(
            """UPDATE games SET name = ?, type = ?, platform = ?, marketplace = ?, source = ?, platform_appid = ?, 
            source_appid = ?, playtime_forever = ?, rtime_last_played = ?, completed = ?, completed_date = ?, rating = ?, 
            link = ?, link2 = ?, header_image = ?, short_description = ?, hide = ?, metadata = ? WHERE id = ?""",
            (
                game.name, game.type, game.platform, game.marketplace, game.source, game.platform_appid, 
                game.source_appid, game.playtime_forever, game.rtime_last_played, game.completed, 
                game.completed_date, game.rating, game.link, game.link2, game.header_image, 
                game.short_description, game.hide, game.metadata, game.id
            )
        )
        self.db.commit()

    def delete_game(self, game_id):
        """ Delete a game """
        c = self.db.cursor()
        c.execute("DELETE FROM games WHERE id = ?", (game_id,))
        self.db.commit()

    def close_db(self):
        """ Close the database connection """
        if self.db:
            self.db.close()
            print("Database connection closed.")

