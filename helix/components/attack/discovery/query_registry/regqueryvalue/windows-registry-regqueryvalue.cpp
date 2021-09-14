#include <windows.h>
#include <iostream>

int ${windows_registry_regqueryvalue}(int argc, char*argv[])
{
    NTSTATUS status;
	HKEY hKey;
    CHAR szBuffer[512];
    DWORD dwBufferSize = sizeof(szBuffer);

    status = RegOpenKeyEx(${hive}, ${path}, 0, KEY_READ | KEY_WOW64_64KEY, &hKey);

    if(status) {
        return 1;
    }

    status = RegQueryValueEx(hKey, ${key}, 0, NULL, (LPBYTE)szBuffer, &dwBufferSize);

    if(status) {
        return 1;
    }

    std::cout << szBuffer << std::endl;

    return status;
}
