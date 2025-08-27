#include <windows.h>
#include <stdio.h>

char* generate_flag(int level) {
    static char flag[64];
    DWORD seed = GetTickCount() ^ 0xDEADBEEF;
    sprintf(flag, "flag{level_%d_%08x}", level, seed);
    return flag;
}

int main() {
    printf("[LAB-9] Level 1: Baby Steps\n");
    printf("[*] Checking for debugger...\n");
    
    if (!IsDebuggerPresent()) {
        printf("[!] No debugger detected! Access denied.\n");
        printf("[!] Try to bypass this check by patching.\n");
        return 1;
    }
    
    printf("[+] Debugger detected!\n");
    printf("[+] Congratulations! You've bypassed the check.\n");
    printf("[+] Flag: %s\n", generate_flag(1));
    
    system("pause");
    return 0;
} 