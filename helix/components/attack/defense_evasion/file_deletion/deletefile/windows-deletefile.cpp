#include <windows.h>

int ${windows_deletefile}(int argv, char* argc[]){
    DeleteFileA(${path});

    return 0;
}
