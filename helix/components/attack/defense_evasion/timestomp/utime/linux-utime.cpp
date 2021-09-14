#include <time.h>
#include <utime.h>
#include <sys/stat.h>

int ${linux_utime}(int argv, char* argc[]){
    struct stat fstat;
    struct tm tm;
    struct utimbuf utimbuf;

    strptime(${timestamp}, "%Y-%m-%d %H:%M:%S", &tm);

    stat(${path}, &fstat);

    utimbuf.actime = fstat.st_atime;
    utimbuf.modtime = mktime(&tm);

    utime(${path}, &utimbuf);

    return 0;
}
