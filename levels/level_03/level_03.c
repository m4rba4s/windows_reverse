#include <windows.h>
#include <stdio.h>

char* generate_flag(int level) {
    static char flag[64];
    DWORD seed = GetTickCount() ^ 0xDEADBEEF;
    sprintf(flag, "flag{level_%d_%08x}", level, seed);
    return flag;
}

int main() {
    printf("[LAB-9] Level 3: Packed Surprise\n");
    printf("[*] This binary is packed with UPX...\n");
    printf("[*] Performing timing-based debugger check...\n");
    
    DWORD start_time = GetTickCount();
    
    if (!IsDebuggerPresent()) {
        printf("[!] IsDebuggerPresent detected no debugger!\n");
        return 1;
    }
    
    DWORD end_time = GetTickCount();
    DWORD elapsed = end_time - start_time;
    
    if (elapsed > 100) {
        printf("[!] Timing check failed! Execution took too long.\n");
        printf("[!] Try to bypass both the packer and timing check.\n");
        return 1;
    }
    
    printf("[+] UPX unpacked and timing check passed!\n");
    printf("[+] Congratulations! You've bypassed UPX and timing detection.\n");
    printf("[+] Flag: %s\n", generate_flag(3));
    
    system("pause");
    return 0;
} 