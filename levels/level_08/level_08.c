#include <windows.h>
#include <stdio.h>

char* generate_flag(int level) {
    static char flag[64];
    DWORD seed = GetTickCount() ^ 0xDEADBEEF;
    sprintf(flag, "flag{level_%d_%08x}", level, seed);
    return flag;
}

BOOL check_hardware_breakpoints() {
    CONTEXT ctx;
    ctx.ContextFlags = CONTEXT_DEBUG_REGISTERS;
    
    if (!GetThreadContext(GetCurrentThread(), &ctx)) {
        return TRUE;
    }
    
    if (ctx.Dr0 != 0 || ctx.Dr1 != 0 || ctx.Dr2 != 0 || ctx.Dr3 != 0) {
        return TRUE;
    }
    
    return FALSE;
}

BOOL check_software_breakpoints() {
    HMODULE kernel32 = GetModuleHandleA("kernel32.dll");
    if (!kernel32) return TRUE;
    
    BYTE* isdebugger = (BYTE*)GetProcAddress(kernel32, "IsDebuggerPresent");
    if (!isdebugger) return TRUE;
    
    if (isdebugger[0] == 0xCC) {
        return TRUE;
    }
    
    return FALSE;
}

int main() {
    printf("[LAB-9] Level 8: Hardware Breakpoint Detection\n");
    printf("[*] Checking for hardware and software breakpoints...\n");
    
    if (!IsDebuggerPresent()) {
        printf("[!] IsDebuggerPresent detected no debugger!\n");
        return 1;
    }
    
    if (check_hardware_breakpoints()) {
        printf("[!] Hardware breakpoints detected!\n");
        printf("[!] Try to bypass hardware breakpoint detection.\n");
        return 1;
    }
    
    if (check_software_breakpoints()) {
        printf("[!] Software breakpoints detected!\n");
        printf("[!] Try to bypass software breakpoint detection.\n");
        return 1;
    }
    
    printf("[+] No breakpoints detected!\n");
    printf("[+] Congratulations! You've bypassed breakpoint detection.\n");
    printf("[+] Flag: %s\n", generate_flag(8));
    
    system("pause");
    return 0;
} 