from math import floor, ceil

def byte2str(b):
    return '{0:0>8}'.format(bin(int.from_bytes(b, byteorder="big")).lstrip('0b'))

def bytes2strs(bs):
    bigStr = bin(int.from_bytes(bs, byteorder="big")).lstrip('0b')
    print(bigStr)
    strs = []
    
    firstBitEndIndex = len(bigStr) % 8
    firstBit = bigStr[0:firstBitEndIndex]
    strs.append('{0:0>8}'.format(firstBit))

    for sevenBits in range(floor(len(bigStr)/8)):
        indexStart = firstBitEndIndex + sevenBits*8
        byte = bigStr[indexStart:indexStart+8]
        strs.append(byte)

    return strs

# Variable Length Binary to Integer
def VLB2Int(binList):
    bigBinaryNum = ''
    for byte in binList:
        bigBinaryNum += byte[1:]
        if byte[0] == '0':
            break
    return int(bigBinaryNum, 2)

# Integer to Variable Length Binary
def int2VLB(num):
    binNum = bin(num).lstrip('0b')
    VLB = []
    
    firstBitEndIndex = len(binNum)%7
    firstBit = binNum[0:firstBitEndIndex]
    VLB.append('1' + '{0:0>7}'.format(firstBit))

    for sevenBits in range(floor(len(binNum)/7)):
        indexStart = firstBitEndIndex + sevenBits*7
        byte = '1' + binNum[indexStart:indexStart+7]
        VLB.append(byte)
    
    VLB[-1] = '0' + VLB[-1][1:]

    return VLB
    

def appendMidi(pathSrc1, pathSrc2, pathDst):
    def checkSameHeader(f1, f2):
        f1.read(8)
        midiFormat1 = int.from_bytes(f1.read(2), byteorder='big')
        midiTracks1 = int.from_bytes(f1.read(2), byteorder='big')
        midiDivision1 = int.from_bytes(f1.read(2), byteorder='big')
        f2.read(8)
        midiFormat2 = int.from_bytes(f2.read(2), byteorder='big')
        midiTracks2 = int.from_bytes(f2.read(2), byteorder='big')
        midiDivision2 = int.from_bytes(f2.read(2), byteorder='big')

        f1.seek(0)
        f2.seek(0)

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

        numTracks1 = int(bytes2strs(headerChunk1[2])[0] +
                         bytes2strs(headerChunk1[2])[1], 2)
        numTracks2 = int(bytes2strs(headerChunk2[2])[0] +
                         bytes2strs(headerChunk2[2])[1], 2)
        totalTrackCount = numTracks1 + numTracks2

        # Escrevendo o header modificado
        fileOut.write(bytes("MThd", "ascii"))
        fileOut.write((6).to_bytes(4, byteorder='big', signed=False)) # tamanho dos dados do header
        fileOut.write((2).to_bytes(2, byteorder='big', signed=False)) # tipo de midi
        fileOut.write((2).to_bytes(totalTrackCount, byteorder='big', signed=False)) # numero de tracks
        fileOut.write((128).to_bytes(2, byteorder='big', signed=False)) # divisão: informação de unidade de delta-time
        # fileOut.write(headerChunk1[2]) # divisão: informação de unidade de delta-time

        # Achando o maior delay para a(s) segunda(s) track(s) (soma de delta times)
        max_delta_time_sum = 0
        current_delta_time_sum = 0
        for trackChunk in trackChunks1:
            str_bytes = bytes2strs(trackChunk[2])
            delta_time_bytes = []
            current_byte = "10000000"
            i = 0
            while current_byte[0] != '0':
                current_byte = str_bytes[i]
                delta_time_bytes.append(current_byte)
                i += 1
            delta_time = VLB2Int(delta_time_bytes)
            current_delta_time_sum += delta_time

        # Escrevendo os tracks
        trackChunksSum = trackChunks1 + trackChunks2
        for trackChunk in trackChunksSum:
            fileOut.write(bytes("MTrk", "ascii")) # Tipo de chunk: track
            fileOut.write((trackChunk[1]).to_bytes(4, byteorder='big', signed=False)) # Tamanho dos dados
            fileOut.write(trackChunk[2]) # dados das tracks

    fileSrc1.close()
    fileSrc2.close()
    fileOut.close()


if __name__ == "__main__":
    testFile = open("temp.mid", "rb")
    print(bytes2strs(testFile.read(2)))
    testFile.close()
