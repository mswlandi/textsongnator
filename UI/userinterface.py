from Backend.player import Player

import os
import string

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.factory import Factory
from kivy.properties import *
from kivy.uix.popup import Popup
kivy.require("1.11.1")

import pygame

class ErrorPopup(Popup):
    ## init: str -> void
    ## Objective: creates an error Popup with a message that is the given string and has a button to dismiss. 
    def __init__(self, msg):
        self.__closeButton = Button(text='Dismiss')
        Popup.__init__(self, title=msg, content=self.__closeButton, auto_dismiss=False, size_hint=(0.5, 0.2))
        self.__closeButton.bind(on_press=self.dismiss)


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Root(FloatLayout):
    text_input = ObjectProperty(None)
    play = Player()

    ## dismiss_popup: void -> void
    ## Objective: remove pop up from screen.
    def dismiss_popup(self):
        self._popup.dismiss()

    ## show_load: void -> void
    ## Objective: creates the popup with file chooser where the user can choose a file
    ##  to be loaded at text editor.
    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    ## show_save: void -> void
    ## Objective: creates the popup with file chooser where the user can choose where
    ##  the MIDI generated file will be saved.
    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()


    ## load: str str -> void
    ## Objective: put the text loaded from file to text_input attribute.
    def load(self, path, filename):

        if filename[0].endswith('.txt'):
            with open(os.path.join(path, filename[0])) as stream:
                self.text_input.text += stream.read()
        else:
            errorPopup = ErrorPopup("This file " + filename[0] + " is not a .txt.")
            errorPopup.open()
            print("ERROR: This file", filename,"is not a .txt.")

        self.dismiss_popup()

    ## save: str str -> void
    ## Objective: saves the MIDI file into user disk.
    def save(self, path, filename):
        if filename[-4:] != ".mid":
            filename += ".mid"
        try:
            self.play.clear()
            self.play.generateSong(self.text_input.text)
            self.play.saveSong(os.path.join(path, filename))
        except FileNotFoundError:
            if self.play.isThereSong():
                self.play.saveSong(os.path.join(path, filename))
            else:
                errorPopup = ErrorPopup("There is no song to save.")
                errorPopup.open()
                print("ERROR: There is no song to save.")
        except PermissionError:
            errorPopup = ErrorPopup("Already exists a file with this name.")
            errorPopup.open()
            print("ERROR: Already exists a file with this name.")

        self.dismiss_popup()



    ## play_song: void -> void
    ## Objective: it creates the song and then plays it.
    def play_song(self):
        self.play.clear()
        self.play.generateSong(self.text_input.text)
        clock = pygame.time.Clock()
        try:
            self.play.saveSong('temp.mid')
            pygame.mixer.music.load('temp.mid')
            print("INFO: 'temp.mid' loaded!")
            os.remove('temp.mid')
        except pygame.error:
            print("ERROR: File 'temp.mid' not found!")
            return
        except OSError:
            print("ERROR: File 'temp.mid' can't be deleted!")
            return 
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            # check if playback has finished
            clock.tick(30)


class Textsongnator(App):
    pass


if __name__ == '__main__':
    pygame.init()
    # Loading from .kv file
    Factory.register('Root', cls=Root)
    Factory.register('LoadDialog', cls=LoadDialog)
    Factory.register('SaveDialog', cls=SaveDialog)
    Textsongnator().run()
