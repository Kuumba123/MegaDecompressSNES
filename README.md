# MegaMan SNES Compressor + Decompressor
these are 2 programs that take a SNES MegaMan game (MegaMan 7, Rockman and Forte, MegaMan X2,X3)
and can decompress or compress the graphics data of each of the games. Compression ratio 
should be same or better than orignal (based off my testing) also some of the data that use the 
game LZ based compression like format are not always graphics (keep that in mind for the decompressor).

decompress usage `python decompress.py <input_file.sfc> <output_directory> [-c] [-mm7]`
`-mm7 -rmf -mmx2 -mmx3` are the respective flags for each game.
`-c` outputs compressed Data along with uncompressed data.

compress usage `python compress.py <input_file> <output_file>"`
The input_file is the graphics you would like to be compressed , output_file is the name of the file that will be created upon compression.