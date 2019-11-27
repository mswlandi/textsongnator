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
    