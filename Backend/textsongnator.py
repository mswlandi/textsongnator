from Backend.player import Player
from Backend.instrumentSymbol import instrumentSymbol
import os

if __name__ == "__main__":
    play = Player()
    play.setInstrument(instrumentSymbol.PIANO)
    play.generateSong("ABO+çC")
    play.saveSong("out.mid")
