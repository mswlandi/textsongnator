<center> Henry Bernardo Kochenborger de Avila - 00301161 </center>
<center> Marcos Samuel Winkel Landi - 00304688 </center>
------------------

## <center>Trabalho Prático - Fase 1</center>

## 1ª Parte

### Lista de requisitos

- Caixa de texto para entrada
- Botão para tocar música
- Quando o botão para tocar música é apertado, toca a música
- Obedecer a especificação do PDF para interpretar o texto. Funcionalidade:
	- Notas (A, B, C, D, E, F, G)
	- Silêncio (ESPAÇO)
	- Controle de Volume (+, -, ?, .)
	- Repetição de nota/outras funcionalidades (OUI, ELSE)
	- Controle de oitavas (O+, O-, ?, .)
	- Mais de um intrumento (NL)
	- Controle de BPMs (B+, B-)
- Funcionalidades Opcionais (desenvolver se der tempo):
	- CheckBox ou texto de nota contínua/nota "discreta" (com beats)
	- CheckBox ou texto de transição suave entre notas, quando contínua
	- Uso de números para intervalos e controles mais precisos
	- Easter Egg do [Konami Code](https://pt.wikipedia.org/wiki/Código_Konami)



### Estruturação das classes

Utilizando a linguagem Python e a biblioteca [Pyknon](https://github.com/kroger/pyknon), as seguintes classes serão necessárias - todas aquelas  que são citadas abaixo e não estão definidas explicitamente são classes da biblioteca utilizada (exemplo: Note).

Ademais, atributos são definidos por < nome do atributo > : < tipo do atributo >; e operações, por < nome da operação>(< tipos das entradas >) : < tipo da saída >.

- **instrumentSymbol**(enum)
  - PIANO: 0
  - ACOUSTICGUITAR: 25
  - ELECTRICGUITAR: 27
  - VIOLIN: 40
  - VOICE: 54
  - APPLAUSE: 126
- **musicSymbol**(enum):
  - A: 0
  - B: 1
  - C: 2
  - D: 3
  - E: 4
  - F: 5
  - G: 6
  - PAUSE: 7
  - VOLUP: 8
  - VOLDOWN: 9
  - REPEATNOTE: 10
  - OCTAVEUP: 11
  - OCTAVEDOWN: 12
  - RESET: 13
  - INSTRUMENT: 14
  - BPMUP: 15
  - BPMDOWN: 16
  - KEEP: 17
- **musicSymbolDecoder**
  - private:
    - currentCharacter: string
    + symbols: queue < musicSymbol >
  - public:
    - clear(): void
    + decode(string character): void
    + head(): musicSymbol
- **Player**
  - private: 
    - notes: queue < Note >
    + decoder: musicSymbolDecoder
    + instrument: instrumentSymbol
  - public:
       - addNote(Note note): void
       - setVolume(int volume): void
       - repeatNote(): void # Bota outra nota igual a primeira da fila na fila.
       - setInstrument(instrumentSymbol instrument): void
       - setOctave(int oct): void
       - setBeat(int beat): void
       - resetOctave(): void
       - clear(): void
    - readSymbol(symbol instruction): bool
    - readSheetString(string sheet): bool
    - playSong(): void  # Escreve a música em um arquivo, toca ela e exclui o arquivo
    - saveSong(string filename): bool  # Escreve a música em um arquivo

