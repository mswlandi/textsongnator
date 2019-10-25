def appendMidi(pathSrc1, pathSrc2, pathDst):
    def checkSameHeader(f1, f2):
        fileSrc1.read(8)
        midiFormat1 = int.from_bytes(fileSrc1.read(2), byteorder='big')
        midiTracks1 = int.from_bytes(fileSrc1.read(2), byteorder='big')
        midiDivision1 = int.from_bytes(fileSrc1.read(2), byteorder='big')
        fileSrc2.read(8)
        midiFormat2 = int.from_bytes(fileSrc2.read(2), byteorder='big')
        midiTracks2 = int.from_bytes(fileSrc2.read(2), byteorder='big')
        midiDivision2 = int.from_bytes(fileSrc2.read(2), byteorder='big')

        fileSrc1.seek(0)
        fileSrc2.seek(0)

        return (midiFormat1 == midiFormat2 and
                midiTracks1 == midiTracks2 and
                midiDivision1 == midiDivision2)


    def readChunk(f):
        ended = False
        while(not ended):
            chunktype = f.read(4).decode('ascii')

            if not chunktype:
                ended = True
                continue

            dataLength = int.from_bytes(f.read(4), byteorder='big')
            data = f.read(dataLength)
            yield (chunktype, dataLength, data)


    midiPath1 = pathSrc1
    midiPath2 = pathSrc2
    midiOutPath = pathDst

    fileSrc1 = open(midiPath1, "rb+")
    fileSrc2 = open(midiPath2, "rb+")
    fileOut = open(midiOutPath, "wb")

    if not checkSameHeader(fileSrc1, fileSrc2):
        print("ERRO: os headers dos midi são diferentes :/ (psst, tenta comentar esse if no codigo hihi)")
    else:
        headerChunk1 = None
        trackChunks1 = []
        for chunk in readChunk(fileSrc1):
            if chunk[0] == "MThd":
                headerChunk1 = chunk
            elif chunk[0] == "MTrk":
                trackChunks1.append(chunk)

        headerChunk2 = None
        trackChunks2 = []
        for chunk in readChunk(fileSrc2):
            if chunk[0] == "MThd":
                headerChunk2 = chunk
            elif chunk[0] == "MTrk":
                trackChunks2.append(chunk)


        # Escrevendo o header modificado
        fileOut.write(bytes("MThd", "ascii"))
        fileOut.write((6).to_bytes(4, byteorder='big', signed=False)) # tamanho dos dados do chunk
        fileOut.write((2).to_bytes(2, byteorder='big', signed=False)) # tipo de midi
        fileOut.write((2).to_bytes(2, byteorder='big', signed=False)) # numero de tracks
        fileOut.write((128).to_bytes(2, byteorder='big', signed=False)) # divisão: informação de unidade de delta-time
        # fileOut.write(headerChunk1[2]) # divisão: informação de unidade de delta-time

        # Escrevendo os tracks
        trackChunksSum = trackChunks1 + trackChunks2
        for trackChunk in trackChunksSum:
            fileOut.write(bytes("MTrk", "ascii"))
            fileOut.write((trackChunk[1]).to_bytes(4, byteorder='big', signed=False))
            fileOut.write(trackChunk[2])

    fileSrc1.close()
    fileSrc2.close()
    fileOut.close()
