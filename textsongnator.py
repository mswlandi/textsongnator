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
    def __init__(self):
        self.__currentCharacter = ""
        self.__symbols = []

    def __readChar(self):
        try:
            self.__symbols.append(mapping[self.__currentCharacter])
        except KeyError as e:
            print("INFO: ", e, " não tem no dicionario, interpretando como KEEP.")
            self.__symbols.append(musicSymbol.KEEP)
        #print("DEBUG: simbolos lidos: ", self.__symbols)
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
    # O de O+ e O-
    # B de B+ e B-
    def decode(self, char):

        # Lida com os caracteres que são prefixos de outros
        # que foram adicionados ao currentCharacter
        if self.__currentCharacter != '':
            if char in ('+', '-'):
                self.__currentCharacter += char
                self.__readChar()
                return
            else:
                self.__readChar()

        # Lida com os caracteres que são prefixos de outros
        # que recém foram lidos
        if char.upper() in ('B', 'O'):
            self.__currentCharacter = char
        
        # Lida com qualquer outro caractere
        else:
            #print("DEBUG: __currentCharacter: ", self.__currentCharacter)
            self.__currentCharacter = char
            self.__readChar()

class Player:
    def __init__(self):
        self.__notes = []
        self.__volume = 1
        self.__octave = 1
        self.__beat = 1
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
        self.setBeat(self.getBeat + 1)
        return self.getBeat()
    
    def decBeat(self):
        self.setBeat(self.getBeat - 1)
        return self.getBeat()
    
    def resetVolume(self):
        self.__volume = 1

    def clear(self):
        self.__init__()
    
    def addPause(self): # TODO: IMPLEMENTAR
        pass

    def keep(self): # TODO: IMPLEMENTAR
        pass
    
    def readSymbol(self, symbol):
        print("DEBUG: vai ler o simbolo ", symbol)

        if symbol in (musicSymbol.A,
                      musicSymbol.B,
                      musicSymbol.C,
                      musicSymbol.D,
                      musicSymbol.E,
                      musicSymbol.F,
                      musicSymbol.G):
            self.addNote(symbol)
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

    def readSheetString(self, sheet):
        for char in sheet:
            self.__decoder.decode(char)

            symbol = self.__decoder.head()
            while symbol != None:
                self.readSymbol(symbol)
                symbol = self.__decoder.head()
            

# Esta parte do código só é executada se este arquivo
# for executado, não caso seja importado como um módulo.
if __name__ == "__main__":
    play = Player()
    play.readSheetString("AB+BOO-CDEFGH")
