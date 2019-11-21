from enum import Enum
from Backend.instrumentSymbol import instrumentSymbol

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
        if char.upper() in ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'O'):
            self.__currentCharacter = char

        
        # Lida com qualquer outro caractere
        else:
            self.__currentCharacter = char
            self.__readChar()