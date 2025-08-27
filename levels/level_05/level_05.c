#include <windows.h>
#include <stdio.h>

char* generate_flag(int level) {
    static char flag[64];
    DWORD seed = GetTickCount() ^ 0xDEADBEEF;
    sprintf(flag, "flag{level_%d_%08x}", level, seed);
    return flag;
}

typedef BOOL (WINAPI *IsDebuggerPresent_t)(void);
typedef BOOL (WINAPI *CheckRemoteDebuggerPresent_t)(HANDLE, PBOOL);

BOOL check_api_hooking() {
    HMODULE kernel32 = GetModuleHandleA("kernel32.dll");
    if (!kernel32) return TRUE;
    
    IsDebuggerPresent_t original = (IsDebuggerPresent_t)GetProcAddress(kernel32, "IsDebuggerPresent");
    if (!original) return TRUE;
    
    BYTE* ptr = (BYTE*)original;
    if (ptr[0] == 0xE9 || ptr[0] == 0xFF) {
        return TRUE;
    }
    
    return FALSE;
}

int main() {
    printf("[LAB-9] Level 5: API Hooking Detection\n");
    printf("[*] Checking for API hooks...\n");
    
    if (!IsDebuggerPresent()) {
        printf("[!] IsDebuggerPresent detected no debugger!\n");
        return 1;
    }
    
    if (check_api_hooking()) {
        printf("[!] API hooking detected! IsDebuggerPresent has been modified.\n");
        printf("[!] Try to bypass hook detection.\n");
        return 1;
    }
    
    printf("[+] No API hooks detected!\n");
    printf("[+] Congratulations! You've bypassed hook detection.\n");
    printf("[+] Flag: %s\n", generate_flag(5));
    
    system("pause");
    return 0;
} 