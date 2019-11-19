from enum import Enum
from pyknon.genmidi import Midi
from pyknon.music import Note, NoteSeq
import os

class instrumentSymbol(Enum):
    PIANO = 0
    ACOUSTICGUITAR = 24
    ELECTRICGUITAR = 27
    VIOLIN = 40
    VOICE = 52
    APPLAUSE = 126
    AGOGO = 114
    HARPSICHORD = 7
    TUBULARBELLS = 15
    PANFLUTE = 76
    CHURCHORGAN = 20

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
    VOLDOUBLE = 16
    REPEATNOTE = 17
    OCTAVEUP = 18
    OCTAVEDOWN = 19
    RESET = 20
    INSTRUMENT = 21
    BPMUP = 22
    BPMDOWN = 23
    KEEP = 24
    INSTRUMENTHARPSICHORD = 25
    INSTRUMENTTUBULARBELLS = 26
    INSTRUMENTAGOGO = 27
    INSTRUMENTPANFLUTE = 28
    INSTRUMENTCHURCHORGAN = 29
    INSTRUMENTGENERAL1 = 30
    INSTRUMENTGENERAL2 = 31
    INSTRUMENTGENERAL3 = 32
    INSTRUMENTGENERAL4 = 33
    INSTRUMENTGENERAL5 = 34
    INSTRUMENTGENERAL6 = 35
    INSTRUMENTGENERAL7 = 36
    INSTRUMENTGENERAL8 = 37
    INSTRUMENTGENERAL9 = 38
    INSTRUMENTGENERAL0 = 39

class musicSymbolDecoder:
    

    def __init__(self):
        self.__currentCharacter = ""
        self.__symbols = []
        self.__mapping = {
        "A": musicSymbol.A,
        "a": musicSymbol.REPEATNOTE,
        "A#": musicSymbol.a,
        "a#": musicSymbol.a,
        "B": musicSymbol.B,
        "b": musicSymbol.REPEATNOTE,
        "B#": musicSymbol.b,
        "b#": musicSymbol.b,
        "C": musicSymbol.C,
        "c": musicSymbol.REPEATNOTE,
        "C#": musicSymbol.c,
        "c#": musicSymbol.c,
        "D": musicSymbol.D,
        "d": musicSymbol.REPEATNOTE,
        "D#": musicSymbol.d,
        "d#": musicSymbol.d,
        "E": musicSymbol.E,
        "e": musicSymbol.REPEATNOTE,
        "F": musicSymbol.F,
        "f": musicSymbol.REPEATNOTE,
        "F#": musicSymbol.f,
        "f#": musicSymbol.f,
        "G": musicSymbol.G,
        "g": musicSymbol.REPEATNOTE,
        "G#": musicSymbol.g,
        "g#": musicSymbol.g,
        "+": musicSymbol.VOLUP,
        "-": musicSymbol.VOLDOWN,
        "O": musicSymbol.INSTRUMENTHARPSICHORD,
        "o": musicSymbol.INSTRUMENTHARPSICHORD,
        "I": musicSymbol.INSTRUMENTHARPSICHORD,
        "i": musicSymbol.INSTRUMENTHARPSICHORD,
        "U": musicSymbol.INSTRUMENTHARPSICHORD,
        "u": musicSymbol.INSTRUMENTHARPSICHORD,
        "O+": musicSymbol.OCTAVEUP,
        "O-": musicSymbol.OCTAVEDOWN,
        "?": musicSymbol.OCTAVEUP,
        ".": musicSymbol.RESET,
        "\n": musicSymbol.INSTRUMENTTUBULARBELLS,
        "B+": musicSymbol.BPMUP,
        "B-": musicSymbol.BPMDOWN,
        " ": musicSymbol.VOLDOUBLE,
        "!": musicSymbol.INSTRUMENTAGOGO,
        "1": musicSymbol.INSTRUMENTGENERAL1,
        "2": musicSymbol.INSTRUMENTGENERAL2,
        "3": musicSymbol.INSTRUMENTGENERAL3,
        "4": musicSymbol.INSTRUMENTGENERAL4,
        "5": musicSymbol.INSTRUMENTGENERAL5,
        "6": musicSymbol.INSTRUMENTGENERAL6,
        "7": musicSymbol.INSTRUMENTGENERAL7,
        "8": musicSymbol.INSTRUMENTGENERAL8,
        "9": musicSymbol.INSTRUMENTGENERAL9,
        "0": musicSymbol.INSTRUMENTGENERAL0,
        ";": musicSymbol.INSTRUMENTPANFLUTE,
        ",": musicSymbol.INSTRUMENTCHURCHORGAN
        }

    def __readChar(self):
        try:
            self.__symbols.append(self.__mapping[self.__currentCharacter])

        # Coloca um KEEP por caractere no currentCharacter
        # para lidar com O#, C+ e similares da maneira certa
        except KeyError as e:

            print("INFO: ", e, " não tem no dicionario, interpretando como REPEATNOTE.")

            #pylint: disable=unused-variable
            for char in self.__currentCharacter:
                self.__symbols.append(musicSymbol.REPEATNOTE)
        
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

# Classe para guardar partes da
# música que tem um mesmo instrumento.
class Track:
    def __init__(self, notes, instrument):
        self.__notes = notes
        self.__instrument = instrument
    
    def getInstrument(self):
        return self.__instrument

    def getNotes(self):
        return self.__notes
    
    # Inserts silence into beggining (to append to some other track)
    def addPause(self, note):
        firstNote = self.__notes[0]
        n = Note("A")
        n.octave = firstNote.octave
        n.volume = 0
        n.dur = firstNote.dur
        self.__notes.append(note)

class Player:
    def __init__(self, instrument = instrumentSymbol.PIANO, volume = 100, octave = 5, beat = 150):
        # notes e instrument são variáveis de "buffer" para criar Tracks e adicioná-las ao tracks
        self.__notes = []
        self.__instrument = instrument
        self.__tracks = []
        self.__instrumentIter = iter(instrumentSymbol)
        next(self.__instrumentIter) # o primeiro next é o primeiro instrumento
        self.__volume = volume
        self.__octave = octave
        self.__beat = beat
        self.__decoder = musicSymbolDecoder()

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

    def doubleVolume(self):
        self.setVolume((self.getVolume()*2)%(256-100) + 100)
        return self.getVolume()

    def repeatNote(self):
        if self.__notes != []:
            self.__notes.append(self.__notes[-1])

    def __addTrack(self):
        self.__tracks.append(Track(self.__notes, self.__instrument))
        self.__notes = []
    
    def setInstrument(self, instrument):
        if self.__instrument != instrument:
            self.__addTrack()
            self.__instrument = instrument

    def getInstrument(self):
        return self.__instrument
    
    def incInstrument(self):
        nextInstrument = next(self.__instrumentIter)
        self.setInstrument(nextInstrument)

    def setGeneralInstrument(self, number):
        nextInstrument = self.getInstrument()
        for i in range(0, number):
            try:
                nextInstrument = next(self.__instrumentIter)
            except:
                self.__instrumentIter = iter(instrumentSymbol)
                nextInstrument = instrumentSymbol.PIANO
            
        self.setInstrument(nextInstrument)

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
        elif symbol == musicSymbol.VOLDOUBLE:
            self.doubleVolume()
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
        elif symbol in musicSymbol:
            if symbol.name[0:-1] == "INSTRUMENTGENERAL":
                self.setGeneralInstrument(int(symbol.name[-1]))
            elif symbol.name[0:10] == "INSTRUMENT":
                self.setInstrument(instrumentSymbol[symbol.name[10:]])
        elif symbol == musicSymbol.BPMUP:
            self.incBeat()
        elif symbol == musicSymbol.BPMDOWN:
            self.decBeat()
        elif symbol == musicSymbol.KEEP:
            self.keep()

    def saveSong(self, filename):
        def nameFile(filename, iterator):
            return "".join(filename.split(".")[:-1]) + str(iterator) + "." + filename.split(".")[-1]

        if self.__notes != []:
            self.__addTrack()

        fileNameIterator = 0
        for track in self.__tracks:
            midi = Midi(number_tracks=1, instrument=track.getInstrument().value)
            notes = NoteSeq(track.getNotes())
            midi.seq_notes(notes, track=0)

            midi.write(nameFile(filename, fileNameIterator))
            fileNameIterator += 1
        
        fileNameIterator -= 1
        if fileNameIterator > 0:
            for i in range(fileNameIterator):
                os.system("python midisox.py --combine concatenate " +
                           nameFile(filename, i) + " " +
                           nameFile(filename, i+1) + " " +
                           nameFile(filename, i+1))
                os.remove(nameFile(filename, i))
        
        if os.path.exists(filename):
            os.remove(filename)

        os.rename(nameFile(filename, fileNameIterator), filename)

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

    def generateSong(self, sheet):
        self.readSheetString(sheet)

            

# Esta parte do código só é executada se este arquivo
# for executado, não caso seja importado como um módulo.
if __name__ == "__main__":
    play = Player()
    play.setInstrument(instrumentSymbol.PIANO)
    play.generateSong("B+B+B+B+EEE\nCEGO-\nGO+CO-GE\nABA#A\nGO+EGA\nFGECDO-B")
    play.saveSong("out.mid")
    # os.system(".\\out.mid")
