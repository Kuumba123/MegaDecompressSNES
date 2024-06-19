import os
import sys


CHR_POINTERS_OFFSETS = [0xE993,0x1E391,0x37A01,0x37732] #MM7,MM&B,MMX2,MMX3
MAX_CHR_COUNT = [0xB8,0x100,0xA5,0xDD]

outputCompress = False
gameId = -1

def decompressChr(inputPath: str,outputDirectory: str):
    if not os.path.exists(outputDirectory):
        os.mkdir(outputDirectory)
    
    if not os.path.exists(inputPath):
        print("ERROR: input rom could not be found")
        return

    with open(inputPath, "rb") as file:
        romData = file.read()


    lowRom = False
    if gameId > 1:
        lowRom = True
    
    chrInfoOffset = CHR_POINTERS_OFFSETS[gameId]

    print(f"Decompressing - {MAX_CHR_COUNT[gameId]:X} sets with the info at offset - {chrInfoOffset}")
    
    for i in range(MAX_CHR_COUNT[gameId]):
        addr = int.from_bytes(romData[chrInfoOffset + i * 5:chrInfoOffset + 3 + i * 5],byteorder='little')
        size = int.from_bytes(romData[chrInfoOffset + i * 5 + 3:chrInfoOffset + 5 + i * 5],byteorder='little')

        offset = 0
        if not lowRom:
            offset = addr - 0xC00000
        else:
            offset = (addr & 0x7FFF) + ((addr >> 16) & 0x7F) * 0x8000
        data = bytearray()
        compressedData = bytearray()
        #decompression variables
        controlB = romData[offset]
        offset += 1
        controlC = 8 #count
        writeOffset = 0

        compressedData.append(controlB)

        while True:
            if (controlB & 0x80) == 0:
                data.append(romData[offset])
                compressedData.append(romData[offset])
                writeOffset += 1
                size -= 1
                offset += 1
            else:   #Copy from Window
                windowPosition = (romData[offset] & 3) << 8
                windowPosition |= romData[offset + 1]
                compressedData.append(romData[offset])
                compressedData.append(romData[offset + 1])
                length = romData[offset] >> 2
                for j in range(length):
                    val = data[writeOffset - windowPosition]
                    data.append(val)
                    writeOffset += 1

                #done copying
                size -= length
                offset += 2
            
            if size < 1:
                break
            controlB <<= 1
            controlC -= 1

            if controlC == 0:
                #get new control byte
                controlC = 8
                controlB = romData[offset]
                compressedData.append(romData[offset])
                offset += 1
        
        #save file
        with open(os.path.join(outputDirectory,f"CHR_{i:X}.BIN"),"wb") as outputFile:
            outputFile.write(data)
        if outputCompress == True:
            with open(os.path.join(outputDirectory,f"COMPRESSED_CHR_{i:X}.BIN"),"wb") as outputFile:
                outputFile.write(compressedData)
        #####
    #Done
    print("Decompression Completed")





#Start of the Program
if len(sys.argv) < 3:
    print("Made by PogChampGuy AKA Kuumba")
    print("This Program is used for extracting Compressed CHR Data from MegaMan SNES Games")
    print("Works for the following games:\n\tMegaMan 7\n\tRockman & Forte\n\tMegaMan X2\n\tMegaMan X3\n")
    print("Usage: python decompress.py <input_file.sfc> <output_directory> [-c] [-mm7]\n")
    print("-mm7\t\tSpecifier for MegaMan 7")
    print("-rmf\t\tSpecifier for Rockman And Forte")
    print("-mmx2\t\tSpecifier for MegaMan X2")
    print("-mmx3\t\tSpecifier for MegaMan X3")
    print("-c\t\tOutput Compressed Data along with uncompressed data")
else:

    for i in range(len(sys.argv)):
        if sys.argv[i] == "-c":
            outputCompress = True
        if sys.argv[i] == "-mm7":
            gameId = 0
        elif sys.argv[i] == "-rmf":
            gameId = 1
        elif sys.argv[i] == "-mmx2":
            gameId = 2
        elif sys.argv[i] == "-mmx3":
            gameId = 3

    if gameId == -1:
        print("ERROR: game must be specified!")
    else:
        decompressChr(sys.argv[1],sys.argv[2])