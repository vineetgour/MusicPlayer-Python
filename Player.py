import Model
from pygame import mixer
from tkinter import filedialog
import os
from mutagen.mp3 import MP3


class Player:

    def __init__(self):
        mixer.init()
        self.my_model = Model.Model()

    def get_db_status(self):
        return self.my_model.get_db_status()

    def close_player(self):
        mixer.music.stop()
        self.my_model.close_db_connection()

    def set_volume(self, volume_level):
        mixer.music.set_volume(volume_level)

    def add_song(self):
        song_path = filedialog.askopenfilename(title="Select song", filetype=[("mp3 files", ".mp3")])
        if song_path == "":
            return

        song_name = os.path.basename(song_path)
        print("Song path is:", song_path)
        print("Song name is:", song_name)
        self.my_model.add_song(song_name, song_path)
        return song_name

    def remove_song(self, song_name):
        self.my_model.remove_song(song_name)

    def get_song_length(self, song_name):
        self.song_path = self.my_model.get_song_path(song_name)
        self.obj = MP3(self.song_path)
        return self.obj.info.length

    def play_song(self):
        mixer.quit()
        mixer.init(frequency=self.obj.info.sample_rate)
        mixer.music.load(self.song_path)
        mixer.music.play()

    def stop_song(self):
        mixer.quit()

    def pause_song(self):
        mixer.music.pause()

    def unpause_song(self):
        mixer.music.unpause()

    def add_song_to_favourites(self, song_name):
        return self.my_model.add_song_to_favourites(song_name, self.my_model.get_song_path(song_name))

    def load_song_from_favourites(self):
        return self.my_model.load_songs_from_favourites(), self.my_model.song_dict

    def remove_song_from_favourites(self, song_name):
        return self.my_model.remove_song_from_favourites(song_name)

if __name__ == "__main__":
    p=Player()
    print("Db connection:", p.get_db_status())
    p.add_song()
