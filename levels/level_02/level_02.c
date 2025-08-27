#include <windows.h>
#include <stdio.h>

char* generate_flag(int level) {
    static char flag[64];
    DWORD seed = GetTickCount() ^ 0xDEADBEEF;
    sprintf(flag, "flag{level_%d_%08x}", level, seed);
    return flag;
}

int main() {
    printf("[LAB-9] Level 2: Remote Check\n");
    printf("[*] Performing multiple debugger checks...\n");
    
    BOOL isDebuggerPresent = FALSE;
    BOOL isRemoteDebuggerPresent = FALSE;
    
    if (!IsDebuggerPresent()) {
        printf("[!] IsDebuggerPresent detected no debugger!\n");
        isDebuggerPresent = TRUE;
    }
    
    if (CheckRemoteDebuggerPresent(GetCurrentProcess(), &isRemoteDebuggerPresent)) {
        if (!isRemoteDebuggerPresent) {
            printf("[!] CheckRemoteDebuggerPresent detected no remote debugger!\n");
            return 1;
        }
    }
    
    if (isDebuggerPresent || !isRemoteDebuggerPresent) {
        printf("[!] Multiple debugger checks failed!\n");
        printf("[!] Try to bypass both IsDebuggerPresent and CheckRemoteDebuggerPresent.\n");
        return 1;
    }
    
    printf("[+] All debugger checks passed!\n");
    printf("[+] Congratulations! You've bypassed multiple anti-debug checks.\n");
    printf("[+] Flag: %s\n", generate_flag(2));
    
    system("pause");
    return 0;
} 