import sys


def compressChr(inputPath: str,output_file: str):
    WINDOW_SIZE = 0x3FF
    MAX_LENGTH = 0x3F
    
    with open(inputPath, "rb") as inputFile:
        inputData = inputFile.read()

    compressedData = []
    compressedBytes = bytearray()
    i = 0
    dataLength = len(inputData)

    print("attempting to find matches")

    while i < len(inputData):
        matchLength = 0
        matchDistance = 0
        
        #Look back within the window to find the longest match (if possible)
        j = 1
        while j <= min(WINDOW_SIZE, i):
            substringLength = 0

            #Find the length of the match starting from the current position
            #Make sure we don't go out of bounds in the string
            while (substringLength < min(min(dataLength - i, WINDOW_SIZE), MAX_LENGTH) and
                    (i - j + substringLength) < dataLength and
                    inputData[i - j + substringLength] == inputData[i + substringLength]):
                substringLength += 1
            
            #Update matchLength and matchDistance if a longer match is found
            if substringLength > matchLength:
                matchLength = substringLength
                matchDistance = j
            j += 1
        ##############

        #If a match is found, add a tuple (distance, length, next character) to the compressed data
        #Also check to see if there is still space left to look ahead
        if matchLength > 1 and (i + matchLength) < dataLength and (dataLength - i) > 3:
            compressedData.append((matchDistance, matchLength, inputData[i + matchLength]))
            i += matchLength
        else:
            #No match was found
            compressedData.append((0, 0,inputData[i]))
            i += 1
    ###########

    #Convert to SNES MegaMan format (Complete)

    controlB = 0
    controlC = 8
    offset = 0

    print("ouputing compressed data")

    for distance, length, next_char in compressedData:

        #unique byte (no match)
        if length == 0:
            compressedBytes.append(next_char)
        else:
            controlB |= 1
            compressedBytes.append(((length) << 2) + (distance >> 8))
            compressedBytes.append((distance & 0xFF))

        controlC -= 1

        if controlC == 0:
            #add to start of set
            controlC = 8
            compressedBytes.insert(offset,controlB)
            controlB = 0
            offset = len(compressedBytes)
        else:
            controlB <<= 1

    if controlC < 8: #check if control byte has been written
        controlB <<= (controlC - 1)
        compressedBytes.insert(offset,controlB)

    #Done
    if output_file == "":
        output_file = f"COMPRESSED_{inputPath}"
    with open(output_file,"wb") as outputFile:
        outputFile.write(compressedBytes)
    print(f"The file - {inputPath} has been compressed")
    print(f"Compressed Size: {len(compressedBytes):X}  Uncompressed Size: {dataLength:X}")

#Start of the Program
if len(sys.argv) < 3:
    print("Made by PogChampGuy AKA Kuumba")
    print("This Program is used for Compressing CHR Data for MegaMan 7, MegaMan X2/X3 and MegaMan & Bass")
    print("Usage: python compress.py <input_file> <output_file>")
else:
    output_file = ""
    if len(sys.argv) == 3:
        output_file = sys.argv[2]
    compressChr(sys.argv[1],output_file)