from enum import Enum
import pyknon

class instrumentSymbol(Enum):
    PIANO = 0
    ACOUSTICGUITAR = 25
    ELECTRICGUITAR = 27
    VIOLIN = 40
    VOICE = 54
    APPLAUSE = 126

class musicSymbol(Enum):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    F = 5
    G = 6
    PAUSE  = 7
    VOLUP = 8
    VOLDOWN = 9
    REPEATNOTE = 10
    OCTAVEUP = 11
    OCTAVEDOWN = 12
    RESET = 13
    INSTRUMENT = 14
    BPMUP = 15
    BPMDOWN = 16
    KEEP = 17

mapping = {
    "A": musicSymbol.A,
    "a": musicSymbol.A,
    "B": musicSymbol.B,
    "b": musicSymbol.B,
    "C": musicSymbol.C,
    "c": musicSymbol.C,
    "D": musicSymbol.D,
    "d": musicSymbol.D,
    "E": musicSymbol.E,
    "e": musicSymbol.E,
    "F": musicSymbol.F,
    "f": musicSymbol.F,
    "G": musicSymbol.G,
    "g": musicSymbol.G,
    "+": musicSymbol.VOLUP,
    "-": musicSymbol.VOLDOWN,
    "O": musicSymbol.REPEATNOTE,
    "o": musicSymbol.REPEATNOTE,
    "I": musicSymbol.REPEATNOTE,
    "i": musicSymbol.REPEATNOTE,
    "U": musicSymbol.REPEATNOTE,
    "u": musicSymbol.REPEATNOTE,
    "O+": musicSymbol.OCTAVEUP,
    "O-": musicSymbol.OCTAVEDOWN,
    "?": musicSymbol.RESET,
    ".": musicSymbol.RESET,
    "\n": musicSymbol.INSTRUMENT,
    "B+": musicSymbol.BPMUP,
    "B-": musicSymbol.BPMDOWN
    }

class musicSymbolDecoder:
    __currentCharacter = ""
    __symbols = []

    def clear(self):
        self.__currentCharacter = ""
        self.__symbols = []

    def head(self):
        return self.__symbols.pop()

    def decode(self, string):
        if mapping[string] != None:
            self.__symbols.append(mapping[string])
        else:
            self.__symbols.append(musicSymbol.KEEP)

class Player:
    __notes = []
    __volume = 1
    __octave = 1
    __beat = 1
    __decoder = musicSymbolDecoder()
    __instrument = instrumentSymbol.PIANO

    def addNote(self, note):
        self.__notes.append(note)

    def setVolume(self, vol):
        if vol >= 0:
            self.__volume = vol

    def getVolume(self):
        return self.__volume

    def repeatNote(self):
        if self.__notes != []:
            self.__notes.append(self.__notes[0])

    def setInstrument(self, instrument):
        self.__instrument = instrument

    def getInstrument(self):
        return self.__instrument

    def setOctave(self, oct):
        self.__octave = oct

    def getOctave(self):
        return self.__octave

    def setBeat(self, bpm):
        if bpm > 0:
            self.__beat = bpm

    def getBeat(self):
        return self.__beat

    def resetOctave(self):
        self.__octave = 1

    def clear(self):
        self.__notes = []
        self.__volume = 1
        self.__octave = 1
        self.__beat = 1
        self.__decoder = musicSymbolDecoder()
        self.__instrument = instrumentSymbol.PIANO
