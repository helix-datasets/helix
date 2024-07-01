#include <stdio.h>
#include <string.h>

void ${new_file}(){

    FILE *fpoint;

    char fileData[50]= "Hello, this is a warning";

    fpoint = fopen("/home/gl33203/.test.txt","w");

    if (fpoint == NULL){
        printf("File failed to open.\n");
    }
    else{
        printf("The file is created succesfully.\n");

        if (strlen(fileData) > 0){
            fputs(fileData, fpoint);
            fputs("\n", fpoint);
        }

        fclose(fpoint);
        printf("Data succesfully written in file.\n");
    }

    return 0;
}
