import os
import sys


CHR_POINTERS_OFFSETS = [0xE993] #MM7,MMX1


def decompressChr(inputPath: str,outputDirectory: str):
    if not os.path.exists(outputDirectory):
        os.mkdir(outputDirectory)
    
    with open(inputPath, "rb") as file:
        romData = file.read()

    chrInfoOffset = CHR_POINTERS_OFFSETS[0]

    lowRom = False
    
    for i in range(0xB0):
        addr = int.from_bytes(romData[chrInfoOffset + i * 5:chrInfoOffset + 3 + i * 5],byteorder='little')
        size = int.from_bytes(romData[chrInfoOffset + i * 5 + 3:chrInfoOffset + 5 + i * 5],byteorder='little')

        offset = 0
        if not lowRom:
            offset = addr - 0xC00000
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
        with open(os.path.join(outputDirectory,f"COMPRESSED_CHR_{i:X}.BIN"),"wb") as outputFile:
            outputFile.write(compressedData)
        #####





#Start of the Program
if len(sys.argv) != 3:
    print("Made by PogChampGuy AKA Kuumba")
    print("This Program is used for extracting Compressed CHR Data from MegaMan 7")
    print("Usage: python decompress.py <input_file> <output_directory>")
else:
    decompressChr(sys.argv[1],sys.argv[2])