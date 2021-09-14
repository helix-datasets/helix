#include <stdio.h>
#include <string.h>
#include <zlib.h>

#define CHUNK 1024

int ${linux_decompress_zlib}(int argv, char* argc[]){
    char buffer[CHUNK];

    gzFile compressed = gzopen(${input},"rb");

    if(compressed == NULL)
        return 1;

    FILE *decompressed = fopen(${output}, "wb");

    if(decompressed == NULL)
        return 1;

    while(!gzeof(compressed)) {
        int bytes = gzread(compressed, buffer, CHUNK);
        fwrite(buffer, bytes, 1, decompressed);
    }

    fflush(decompressed);

    gzclose(compressed);
    fclose(decompressed);

    return 0;
}
