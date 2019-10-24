from enum import Enum
from pyknon.genmidi import Midi
from pyknon.music import Note, NoteSeq
import os
# não usados por enquanto:
# from pyknon.notation import *
# from pyknon.pc_sets import *
# from pyknon.pcset import *
# from pyknon.simplemusic import *

class instrumentSymbol(Enum):
    PIANO = 0
    ACOUSTICGUITAR = 24
    ELECTRICGUITAR = 27
    VIOLIN = 40
    VOICE = 52
    APPLAUSE = 126

class musicSymbol(Enum):
    A = 0
    a = 1
    B = 2
    b = 3
    C = 4
    c = 5
    D = 6
    d = 7
    E = 8
    F = 9
    f = 10
    G = 11
    g = 12
    PAUSE  = 13
    VOLUP = 14
    VOLDOWN = 15
    REPEATNOTE = 16
    OCTAVEUP = 17
    OCTAVEDOWN = 18
    RESET = 19
    INSTRUMENT = 20
    BPMUP = 21
    BPMDOWN = 22
    KEEP = 23

mapping = {
    "A": musicSymbol.A,
    "a": musicSymbol.A,
    "A#": musicSymbol.a,
    "a#": musicSymbol.a,
    "B": musicSymbol.B,
    "b": musicSymbol.B,
    "B#": musicSymbol.b,
    "b#": musicSymbol.b,
    "C": musicSymbol.C,
    "c": musicSymbol.C,
    "C#": musicSymbol.c,
    "c#": musicSymbol.c,
    "D": musicSymbol.D,
    "d": musicSymbol.D,
    "D#": musicSymbol.d,
    "d#": musicSymbol.d,
    "E": musicSymbol.E,
    "e": musicSymbol.E,
    "F": musicSymbol.F,
    "f": musicSymbol.F,
    "F#": musicSymbol.f,
    "f#": musicSymbol.f,
    "G": musicSymbol.G,
    "g": musicSymbol.G,
    "G#": musicSymbol.g,
    "g#": musicSymbol.g,
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
    "B-": musicSymbol.BPMDOWN,
    " ": musicSymbol.PAUSE
    }

class musicSymbolDecoder:
    def __init__(self):
        self.__currentCharacter = ""
        self.__symbols = []

    def __readChar(self):
        try:
            self.__symbols.append(mapping[self.__currentCharacter])

        # Coloca um KEEP por caractere no currentCharacter
        # para lidar com O#, C+ e similares da maneira certa
        except KeyError as e:

            print("INFO: ", e, " não tem no dicionario, interpretando como KEEP.")

            #pylint: disable=unused-variable
            for char in self.__currentCharacter:
                self.__symbols.append(musicSymbol.KEEP)
        
        self.__currentCharacter = ''

    def clear(self):
        self.__currentCharacter = ""
        self.__symbols = []

    def head(self):
        if self.__symbols == []:
            return None
        else:
            return self.__symbols.pop(0)

    # Prefixos:
    # {O,B} de {O,B}{-,+}
    # {A-G} de {A-G}#
    def decode(self, char):

        # Lida com os caracteres que são prefixos de outros
        # que foram adicionados ao currentCharacter
        if self.__currentCharacter != '':
            if char in ('+', '-', '#'):
                self.__currentCharacter += char
                self.__readChar()
                return
            else:
                self.__readChar()

        # Lida com os caracteres que são prefixos de outros
        # que recém foram lidos
        if char.upper() in ('A', 'B', 'C', 'D', 'F', 'G', 'O'):
            self.__currentCharacter = char
        
        # Lida com qualquer outro caractere
        else:
            self.__currentCharacter = char
            self.__readChar()

class Player:
    def __init__(self):
        self.__notes = []
        self.__volume = 100
        self.__octave = 5
        self.__beat = 150
        self.__decoder = musicSymbolDecoder()
        self.__instrumentIter = iter(instrumentSymbol)
        self.__instrument = instrumentSymbol.PIANO

    def addNote(self, note):
        self.__notes.append(note)

    def setVolume(self, vol):
        if vol >= 0:
            self.__volume = vol

    def getVolume(self):
        return self.__volume
    
    def incVolume(self):
        self.setVolume(self.getVolume() + 1)
        return self.getVolume()
    
    def decVolume(self):
        self.setVolume(self.getVolume() - 1)
        return self.getVolume()

    def repeatNote(self):
        if self.__notes != []:
            self.__notes.append(self.__notes[-1])

    def setInstrument(self, instrument):
        self.__instrument = instrument

    def getInstrument(self):
        return self.__instrument
    
    def incInstrument(self):
        self.__instrument = self.__instrumentIter.next()

    def setOctave(self, oct):
        self.__octave = oct

    def getOctave(self):
        return self.__octave

    def incOctave(self):
        self.setOctave(self.getOctave() + 1)
        return self.getOctave()
    
    def decOctave(self):
        self.setOctave(self.getOctave() - 1)
        return self.getOctave()
    
    def resetOctave(self):
        self.__octave = 1

    def setBeat(self, bpm):
        if bpm > 0:
            self.__beat = bpm

    def getBeat(self):
        return self.__beat
    
    def incBeat(self):
        self.setBeat(self.getBeat() + 5)
        return self.getBeat()
    
    def decBeat(self):
        self.setBeat(self.getBeat() - 5)
        return self.getBeat()
    
    def resetVolume(self):
        self.__volume = 1

    def clear(self):
        self.__init__()
    
    def addPause(self):
        vol = self.getVolume()
        self.setVolume(0)
        self.addNote(self.symbol2Note(musicSymbol.A))
        self.setVolume(vol)

    def keep(self):
        if self.__notes != []:
            self.__notes[-1].dur += (60/self.getBeat())/4
    
    def symbol2Note(self, symbol):
        if(symbol.name.islower()):
            n = Note(symbol.name.upper()+'#')
        else:
            n = Note(symbol.name)
        n.octave = self.getOctave()
        n.volume = self.getVolume()
        # 60 bpm faz uma batida por segundo, e uma batida é uma semínima (0.25)
        n.dur = (60/self.getBeat())/4

        return n

    def readSymbol(self, symbol):
        print("DEBUG: vai ler o simbolo ", symbol)

        if symbol in (musicSymbol.A,
                      musicSymbol.a,
                      musicSymbol.B,
                      musicSymbol.b,
                      musicSymbol.C,
                      musicSymbol.c,
                      musicSymbol.D,
                      musicSymbol.d,
                      musicSymbol.E,
                      musicSymbol.F,
                      musicSymbol.f,
                      musicSymbol.G,
                      musicSymbol.g):
            self.addNote(self.symbol2Note(symbol))
        elif symbol == musicSymbol.PAUSE:
            self.addPause()
        elif symbol == musicSymbol.VOLUP:
            self.incVolume()
        elif symbol == musicSymbol.VOLDOWN:
            self.decVolume()
        elif symbol == musicSymbol.REPEATNOTE:
            self.repeatNote()
        elif symbol == musicSymbol.OCTAVEUP:
            self.incOctave()
        elif symbol == musicSymbol.OCTAVEDOWN:
            self.decOctave()
        elif symbol == musicSymbol.RESET:
            self.resetOctave()
            self.resetVolume()
        elif symbol == musicSymbol.INSTRUMENT:
            self.incInstrument()
        elif symbol == musicSymbol.BPMUP:
            self.incBeat()
        elif symbol == musicSymbol.BPMDOWN:
            self.decBeat()
        elif symbol == musicSymbol.KEEP:
            self.keep()

    def saveSong(self, filename):
        notes = NoteSeq(self.__notes)
        print(notes)
        midi = Midi(number_tracks=1, instrument=self.__instrument.value)
        midi.seq_notes(notes, track=0)
        midi.write(filename)

    def readSheetString(self, sheet):
        # Função interna para ler os dados devolvidos pelo decoder
        def readDecoderHead():
            symbol = self.__decoder.head()
            while symbol != None:
                self.readSymbol(symbol)
                symbol = self.__decoder.head()
            
        for char in sheet:
            self.__decoder.decode(char)
            readDecoderHead()
        
        # Captura o último caractere, o que é preciso
        # caso ele seja um de prefixo como O
        self.__decoder.decode(" ")
        readDecoderHead()

    def playSong(self, sheet):
        self.readSheetString(sheet)
        self.saveSong("temp.mid")

            

# Esta parte do código só é executada se este arquivo
# for executado, não caso seja importado como um módulo.
if __name__ == "__main__":
    play = Player()
    play.setInstrument(instrumentSymbol.VIOLIN)
    play.playSong("CDE F Gxxx")
    os.system(".\\temp.mid")
    
# TODO: Mudar instrumento no meio da música