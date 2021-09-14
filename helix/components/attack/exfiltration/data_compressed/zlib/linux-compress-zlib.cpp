#include <stdio.h>
#include <string.h>
#include <zlib.h>

#define CHUNK 1024

int ${linux_compress_zlib}(int argv, char* argc[]){
    char buffer[CHUNK];

    FILE *decompressed = fopen(${input}, "rb");

    if(decompressed == NULL)
        return 1;

    gzFile compressed = gzopen(${output},"wb");

    if(compressed == NULL)
        return 1;

    while(fgets(buffer, CHUNK, decompressed) != NULL)
        gzwrite(compressed, buffer, strlen(buffer));

    gzflush(compressed, Z_FULL_FLUSH);

    fclose(decompressed);
    gzclose(compressed);

    return 0;
}
