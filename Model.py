from cx_Oracle import *


class Model:
    def __init__(self):
        self.song_dict = {}
        self.db_status = True
        self.conn = None
        self.cur = None
        try:
            self.conn = connect("mouzikka/music@LAPTOP-6UPFPC7V/xe")
            print("Connected successfully to the DB")
            self.cur = self.conn.cursor()
        except DatabaseError as e:
            self.db_status = False
            print(e)

    def get_db_status(self):
        return self.db_status

    def close_db_connection(self):
        if self.cur is not None:
            self.cur.close()
            print("Cursor closed successfully")
        if self.conn is not None:
            self.conn.close()
            print("Disconnected successfully")

    def add_song(self, song_name, song_path):
        self.song_dict[song_name] = song_path
        print("song added: ",self.song_dict[song_name])

    def get_song_path(self,song_name):
        return self.song_dict[song_name]

    def remove_song(self,song_name):
        self.song_dict.pop(song_name)

    def search_song_in_favourites(self, song_name):
        self.cur.execute("select song_name from myFavourites where song_name=:1", (song_name,))
        song_tuple = self.cur.fetchone()
        if song_tuple is None:
            return False
        else:
            return True

    def add_song_to_favourites(self, song_name, song_path):
        if self.search_song_in_favourites(song_name) is True:
            return "Song Already present in Your Favourites"

        self.cur.execute("Select max(song_id) from myFavourites")
        id_no = self.cur.fetchone()[0]
        next_id = 1
        if id_no is not None:
            next_id = id_no + 1

        self.cur.execute("insert into myFavourites values(:1, :2, :3)", (next_id, song_name, song_path))
        self.conn.commit()
        return "Song added to your favourites"

    def load_songs_from_favourites(self):
        self.cur.execute("select song_name,song_path from myFavourites")
        song_present = False
        for song_name, song_path in self.cur:
            self.song_dict[song_name] = song_path
            song_present = True
        if song_present is True:
            return "List populated from favourites"
        else:
            return "No songs present in favourites"

    def remove_song_from_favourites(self, song_name):
        self.cur.execute("delete from myFavourites where song_name=:1", (song_name,))
        if self.cur.rowcount is 0:
            return "Song not present in favourites"
        else:
            self.song_dict.pop(song_name)
            self.conn.commit()
            return "Song deleted from favourites"
