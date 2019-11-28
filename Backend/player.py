from Backend.instrumentSymbol import instrumentSymbol
from Backend.musicSymbol import musicSymbol, musicSymbolDecoder
from Backend.track import  Track

from pyknon.genmidi import Midi
from pyknon.music import Note, NoteSeq

import os

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
        self.__lastChar = None

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
        if self.getVolume()*2 > 255:
            self.setVolume(100)
        else:
            self.setVolume(self.getVolume()*2)
        return self.getVolume()

    def repeatNote(self):
        if self.__lastChar in ('A', 'B', 'C', 'D', 'E', 'F', 'G'):
            if self.__notes != []:
                self.__notes.append(self.__notes[-1])
        else:
            self.addPause()

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
                os.system("python Backend/Thirdparties/midisox.py --combine concatenate " +
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
            self.__lastChar = char
        
        # Captura o último caractere, o que é preciso
        # caso ele seja um de prefixo como O
        self.__decoder.decode(" ")
        readDecoderHead()

    def generateSong(self, sheet):
        self.readSheetString(sheet)

    ## isThereSong: void -> bool
    ## Objective: if track is not empty, returns true. Else, returns false.
    def isThereSong(self):
        if self.__tracks == []:
            return False
        else:
            return True