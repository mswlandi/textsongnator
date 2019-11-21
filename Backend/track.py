from pyknon.music import Note, NoteSeq

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