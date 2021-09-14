#include <unistd.h>

int ${linux_unlink}(int argv, char* argc[]){
    unlink(${path});

    return 0;
}
