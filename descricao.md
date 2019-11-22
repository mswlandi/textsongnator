_Henry Bernardo Kochenborger de Avila_

_Marcos Samuel Winkel Landi_

## Documentação do programa

​	O programa _textsongnator_ busca gerar arquivos de áudio a partir de qualquer entrada válida de texto. Para isso, foi necessário arbitrariamente escolher caracteres que serviriam para realizar algumas operações sobre este áudio gerado - estas escolhas foram definidas previamente no enunciado da primeira fase do trabalho e, depois, alteradas na terceira.

![Diagrama de casos de uso](https://i.imgur.com/tVWldsg.png)

​	Como este programa deve garantir uma boa relação entre o seu manuseio e usuário, a biblioteca [Kivy](kivy.org) foi escolhida por ser amplamente utilizada para criação de interfaces e, por consequência, existir muito material sobre ela.

![Text Editor](https://imgur.com/ChMlyei.png)

![Buttons](https://imgur.com/faOdTC6.png)

![Load](https://i.imgur.com/EjIZVX0.png)

![Save](https://i.imgur.com/iRSY6Jn.png)





Assim sendo, foi criado um arquivo Python apenas para realizar as operações entre a interface de usuário e a aplicação, possuindo as seguintes classes:

- **LoadDialog**(FloatLayout): é a classe que guarda os _widgets_ que irão possibilitar o usuário carregar um arquivo texto que irá implicar no som gerado pela aplicação. Dessa forma, seus atributos são:

  - load: é o botão que realiza a operação e carrega o texto para a aplicação.

  - cancel: é o botão que a cancela a operação e mantém o texto da aplicação exatamente da mesma forma que estava antes.

- **SaveDialog**(FloatLayout): é a classe referente a parte de salvar o arquivo MIDI. Para isso, é necessário que ela contenha os atributos:

  - save: é o botão que aplica a operação e salva definitivamente o arquivo.
  - text_input: é uma caixa de texto em que o usuário pode escrever o nome do arquivo a ser salvo - junto com o local que irá ser colocado.
  - cancel: é o botão que cancela a operação e não salva o arquivo.

- **Root**(FloatLayout): é a classe que define a interface. Ou seja, ela realiza a ligação entre a aplicação e o usuário e, para isso, possui os seguintes atributos:

  - text_input: é uma caixa de texto que trata-se do local em que o usuário irá escrever o texto que será transformado em áudio quando o botão 'Play Song' for apertado.
  - play: é um objeto da classe Player que, essencialmente, trata-se da classe que irá realizar a transformação do texto em áudio.

  Seus métodos tratam as requisições de carregamento, salvamento ou realizar a transformação do texto em som, sendo eles:

  - dismiss_popup(): retira o _popup_ da tela.
  - show_load(): mostra o _popup_ para escolher o arquivo de texto a ser carregado pelo programa.
  - show_save(): mostra o _popup_ para escolher o nome do arquivo MIDI e o local que ele será salvo.
  - load(path, filename): carrega efetivamente o dado contido no arquivo informado pelo _path\filename_ dentro do atributo text_input.
  - save(path, filename): salva o arquivo dado por _path\filename_.
  - play_song(): salva um arquivo MIDI temporário, gera o som com o objeto _play_ e roda o som gerado na aplicação.

- **Textsongnator**(App): é a própria interface gráfica, definida pelo arquivo _.kv_ de mesmo nome. Este arquivo define o conteúdo da interface, considerando suas páginas, botões, entradas, e realizando as ligações necessárias entre a aplicação e a interface.

E o diagrama de classes da interface gráfica:

![diagrama de classes](https://i.imgur.com/glA68z7.jpg)

​	Sobre a aplicação, a biblioteca [Pyknon](github.com/kroger/pyknon) foi utilizada pois simplifica o tratamento do áudio. Ademais, para garantir algumas das definições impostas pelo enunciado do trabalho, foi necessário utilizar a ferramenta [midisox](pjb.com.au/midi/midisox.html) que permite, por exemplo, concatenar arquivos MIDI, possibilitando que o arquivo possua diversos instrumentos - essa que é uma limitação da biblioteca Pyknon.



![diagrama de classes](https://i.imgur.com/4lSUD0f.png)

​	

​	Para efetivar a funcionalidade do programa, algumas classes foram criadas em outro arquivo Python - as mesmas citadas na fase 1 do projeto, mas com algumas alterações nos seus métodos ou atributos, acrescentadas de uma outra não citada anteriormente -, tais como:

- **instrumentSymbol**(Enum): é uma classe que possui alguns instrumentos padrões que serão utilizados na aplicação, referenciando seu número dentro dos arquivos MIDI.

  - PIANO = 0
  - ACOUSTICGUITAR = 24
  - ELECTRICGUITAR = 27
  - VIOLIN = 40
  - VOICE = 52
  - APPLAUSE = 126
  - AGOGO = 114
  - HARPSICHORD = 7
  - TUBULARBELLS = 15
  - PANFLUTE = 76
  - CHURCHORGAN = 20

- **musicSymbol**(Enum): assim como a classe acima, esta classe apenas define as notas e seus valores que serão utilizados depois para realizar a transformação do texto para áudio. Cada letra maiúscula se refere diretamente a uma nota - por exemplo, A se refere a nota lá (A). Já as letras minúsculas se referem a versão sustenido da sua letra maiúscula - por exemplo, a se refere a nota lá sustenido (A#).

  - A = 0
  - a = 1
  - B = 2
  - b = 3
  - C = 4
  - c = 5
  - D = 6
  - d = 7
  - E = 8
  - F = 9
  - f = 10
  - G = 11
  - g = 12
  - PAUSE = 13
  - VOLUP = 14
  - VOLDOWN = 15
  - VOLDOUBLE = 16
  - REPEATNOTE = 17
  - OCTAVEUP = 18
  - OCTAVEDOWN = 19
  - RESET = 20
  - INSTRUMENT = 21
  - BPMUP = 22
  - BPMDOWN = 23
  - KEEP = 24
  - INSTRUMENTHARPSICHORD = 25
  - INSTRUMENTTUBULARBELLS = 26
  - INSTRUMENTAGOGO = 27
  - INSTRUMENTPANFLUTE = 28
  - INSTRUMENTCHURCHORGAN = 29
  - INSTRUMENTGENERAL1 = 30
  - INSTRUMENTGENERAL2 = 31
  - INSTRUMENTGENERAL3 = 32
  - INSTRUMENTGENERAL4 = 33
  - INSTRUMENTGENERAL5 = 34
  - INSTRUMENTGENERAL6 = 35
  - INSTRUMENTGENERAL7 = 36
  - INSTRUMENTGENERAL8 = 37
  - INSTRUMENTGENERAL9 = 38
  - INSTRUMENTGENERAL0 = 39

  O mapeamento do caractere para um objeto desta classe é feito utilizando um dicionário pré-definido no código.

- **musicSymbolDecoder**: é a classe que realiza as operações de decodificação de um caractere para um _musicSymbol_. Para sua atividade ser concluída, os seguintes atributos foram necessários:

  - *(private)* currentCharacter: é a string que define o que será decodificado no instante atual.
  - _(private)_ symbols: é uma lista de musicSymbols que irá possuir todos os símbolos até então decodificados.

  Além disso, esta classe possui métodos que realizam a decodificação, sendo eles:

  - _(private)_ readChar(): pega o atributo _currentCharacter_ e realiza a decodificação com o dicionário citado anteriormente. Caso não o encontre no dicionário, significa que deve repetir a nota tocada anteriormente. Além disso, apaga a string _currentCharacter_ para poder realizar a sua próxima decodificação.
  - clear(): apaga todos os dados contidos nos seus atributos.
  - head(): retorna o primeiro elemento da lista de símbolos, retirando-o da lista.
  - decode(char): recebe uma string e a decodifica, garantindo que funcione com tamanhos diferentes e codificações com o mesmo prefixo - como no caso de B+ e B. Para isso, chama a função _readChar()_.

- **Track**: esta classe guarda partes da música gerada tal que essa parte possui as notas na mesma sequência em que serão tocadas na música final e os mesmos instrumentos. Dessa maneira, possui os seguintes atributos:

  - _(private)_ notes: é uma lista de notas segundo a definição da classe.
  - _(private)_ instrument: é o instrumento em comum dessas notas.

  Além disso, esta classe possui os seguintes métodos:

  - _builder(notes, instrument)_: é o método de construção da classe que define os atributos _notes_ e _instrument_.
  - getInstrument(): é o método que retorna o atributo _instrument_.
  - getNotes(): é o método que retorna o atributo _notes_.
  - addPause(): esse método foi criado para realizar a concatenação dos arquivos MIDI e, por este motivo, foi necessário adicionar uma pausa - essa que é definida pela adição da nota A com volume nulo - no início do arquivo.

- **Player**: esta classe é a classe que realiza as ligações necessárias para a aplicação. Dessa maneira, ela deve ser vista como uma máquina que possui um decodificador de símbolos, volume, frequência de _beat_, oitava atual e instrumento atual. Assim sendo, seus atributos são:

  - _(private)_ notes: é uma lista de notas - classe Note da biblioteca Pyknon.
  - _(private)_ instrument: é o instrumento atual do áudio gerado - só é relevante durante a decodificação.
  - _(private)_ tracks: é uma lista de objetos da classe _Track_ - citada acima -, guardando áudios com instrumentos diferentes.
  - _(private)_ instrumentIter: é um iterador sobre a classe _instrumentSymbol_.
  - _(private)_ volume: é o volume atual do áudio.
  - _(private)_ octave: é a oitava atual do áudio.
  - _(private)_ beat: é a frequência de batida atual do áudio.
  - _(private)_ decoder: é o decodificador dos caracteres para os símbolos musicais.

  Ademais, esta classe possui métodos:

  - addNote(note): acrescenta um objeto da classe _Note_ no fim do atributo _notes_.
  - setVolume(vol): define o atributo _volume_ da classe para o dado como parâmetro do método.
  - incVolume(): incrementa o atributo _volume_ da classe.
  - decVolume(): decrementa o atributo _volume_ da classe.
  - doubleVolume(): dobra o atributo _volume_ da classe.
  - repeatNote(): repete a última nota acrescentada na lista de notas, colocando-a novamente no final da lista.
  - _(private)_ addTrack(): acrescenta uma nova track a lista de tracks com as notas guardadas até então e o instrumento atual. Após isso, reinicializa a lista de notas da classe.
  - setInstrument(instrument): define o atributo _instrument_ da classe.
  - getInstrument(): retorna o atributo _instrument_ da classe.
  - incInstrument(): define o atributo _instrument_ da classe como o próximo item do iterador _instrumentIter_ - também atributo desta classe.
  - setGeneralInstrument(number): define o atributo _instrument_ da classe como o enésimo item a partir do item dado pelo iterador _instrumentIter_ - possuindo uma definição circular. 
  - setOctave(oct): define o atributo _octave_ da classe.
  - incOctave(): incrementa o atributo _octave_ da classe.
  - decOctave(): decrementa o atributo _octave_ da classe.
  - resetOctave(): define o valor do atributo _octave_ da classe para 1.
  - setBeat(bpm): define o valor do atributo _beat_ da classe em BPM.
  - getBeat(): retorna o valor do atributo _beat_ da classe.
  - incBeat(): incrementa o valor do atributo _beat_ da classe em 5.
  - decBeat(): decrementa o valor do atributo _beat_ da classe em 5.
  - resetVolume(): define o valor do atributo _volume_ da classe para 1.
  - clear(): define todos os valores dos atributos desta classe para os iniciais.
  - addPause(): acrescenta uma nota vazia - uma nota A com volume nulo - a lista de notas.
  - keep(): aumenta a duração da nota anterior em uma semínima.
  - symbol2Note(symbol): recebe um musicSymbol que se refere a uma nota e o decodifica para um objeto da classe Note baseado no dicionário citado anteriormente.
  - readSymbol(symbol): recebe um musicSymbol e o decodifica para uma função desta classe de acordo com o mapeamento realizado.
  - saveSong(filename): salva o áudio dado pela concatenação ordenada de todas as tracks contidas no atributo _tracks_ com o nome e caminho dado como parâmetro.
  - readSheetString(sheet): lê o texto, decodifica-o e coloca dentro do atributo _tracks_ segundo sua organização.
  - generateSong(sheet): gera o som de acordo com a função _readSheetString_.
  - isThereSong(): retorna um valor booleano de acordo com a existência ou não de som.
