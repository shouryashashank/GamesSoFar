import sqlite3 as sqlite
import flet as ft
from datetime import datetime

class Database:
    def __init__(self):
        self.db = None

    def connect_to_db(self):
        try:
            self.db = sqlite.connect("game.db")
            c = self.db.cursor()
            c.execute(
                """CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, 
								  name VARCHAR(100) NOT NULL, 
								  createddate DATETIME NOT NULL, 
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
                                  name VARCHAR(255) NOT NULL,
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

    def read_user_db(self):
        """ Read user data from database """
        c = self.db.cursor()
        c.execute("SELECT * FROM users")
        rows = c.fetchall()
        return rows
    
    def create_user(self, name, steamid, googleid, epicid, gogid, psid, xboxid, nintendoid, metadata):
        """ Create a new user """
        c = self.db.cursor()
        c.execute("INSERT INTO users (name, createddate, steamid, googleid, epicid, gogid, psid, xboxid, nintendoid, metadata) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (name, datetime.now(), steamid, googleid, epicid, gogid, psid, xboxid, nintendoid, metadata))
        self.db.commit()
        return c.lastrowid
    
    def update_user(self, user_id, name, steamid, googleid, epicid, gogid, psid, xboxid, nintendoid, metadata):
        """ Update an existing user """
        c = self.db.cursor()
        c.execute("UPDATE users SET name = ?, steamid = ?, googleid = ?, epicid = ?, gogid = ?, psid = ?, xboxid = ?, nintendoid = ?, metadata = ? WHERE id = ?",
                  (name, steamid, googleid, epicid, gogid, psid, xboxid, nintendoid, metadata, user_id))
        self.db.commit()
    
    # crud op on game

    def read_game_db(self, filters=None, sort_by=None, limit=None):
        """
        Read game data from database with optional filters, sorting, and limit.
        
        :param filters: Dictionary of column-value pairs to filter the results.
        :param sort_by: Column name to sort the results by.
        :param limit: Maximum number of results to return.
        :return: List of rows matching the query.
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
        return rows
    
    def insert_multiple_games(self, games):
        """
        Insert multiple games into the games table.
        
        :param games: List of tuples, where each tuple contains the game data.
        """
        try:
            c = self.conn.cursor()
            c.executemany(
                """INSERT INTO games (name, type, platform, marketplace, source, platform_appid, source_appid, playtime_forever, 
                                    rtime_last_played, completed, completed_date, rating, link, link2, header_image, 
                                    short_description, hide, createddate, metadata) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                games
            )
            self.conn.commit()
            print("Multiple games inserted successfully.")
        except sqlite.DatabaseError as e:
            print("Error: Failed to insert multiple games")
            print(e)

    def update_game(self, game_id, name, type, platform, marketplace, source, platform_appid, source_appid, playtime_forever, 
                    rtime_last_played, completed, completed_date, rating, link, link2, header_image, short_description, hide, metadata):
        """ Update an existing game """
        c = self.db.cursor()
        c.execute("UPDATE games SET name = ?, type = ?, platform = ?, marketplace = ?, source = ?, platform_appid = ?, source_appid = ?, playtime_forever = ?, rtime_last_played = ?, completed = ?, completed_date = ?, rating = ?, link = ?, link2 = ?, header_image = ?, short_description = ?, hide = ?, metadata = ? WHERE id = ?",
                  (name, type, platform, marketplace, source, platform_appid, source_appid, playtime_forever, rtime_last_played, completed, completed_date, rating, link, link2, header_image, short_description, hide, metadata, game_id))
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

    