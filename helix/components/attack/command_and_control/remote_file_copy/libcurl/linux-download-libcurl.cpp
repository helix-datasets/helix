#define CURL_STATICLIB
#include <stdio.h>
#include <curl/curl.h>
#include <string>

size_t ${write_data}(void *ptr, size_t size, size_t nmemb, FILE *stream) {
    size_t written;
    written = fwrite(ptr, size, nmemb, stream);
    return written;
}

int ${linux_download_libcurl}(int argc, char*argv[]) {
    // http://www.cplusplus.com/forum/windows/122859/

    CURL *curl;
    FILE *fp;
    CURLcode res;

    curl = curl_easy_init();

    if (curl) {
        fp = fopen(${output}, "wb");

        curl_easy_setopt(curl, CURLOPT_URL, ${url});
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, ${write_data});
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, fp);
        curl_easy_setopt(curl, CURLOPT_VERBOSE, 1L);

        res = curl_easy_perform(curl);

        curl_easy_cleanup(curl);
        fclose(fp);
    }

    return 0;
}
