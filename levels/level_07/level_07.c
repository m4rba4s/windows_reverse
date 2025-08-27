#include <windows.h>
#include <stdio.h>

char* generate_flag(int level) {
    static char flag[64];
    DWORD seed = GetTickCount() ^ 0xDEADBEEF;
    sprintf(flag, "flag{level_%d_%08x}", level, seed);
    return flag;
}

typedef NTSTATUS (NTAPI *NtQueryInformationProcess_t)(
    HANDLE ProcessHandle,
    ULONG ProcessInformationClass,
    PVOID ProcessInformation,
    ULONG ProcessInformationLength,
    PULONG ReturnLength
);

#define ProcessDebugPort 7
#define ProcessDebugObjectHandle 30
#define ProcessDebugFlags 31

#ifndef NT_SUCCESS
#define NT_SUCCESS(Status) (((NTSTATUS)(Status)) >= 0)
#endif

BOOL check_kernel_debug() {
    HMODULE ntdll = GetModuleHandleA("ntdll.dll");
    if (!ntdll) return TRUE;
    
    NtQueryInformationProcess_t NtQueryInformationProcess = 
        (NtQueryInformationProcess_t)GetProcAddress(ntdll, "NtQueryInformationProcess");
    if (!NtQueryInformationProcess) return TRUE;
    
    ULONG debug_port = 0;
    NTSTATUS status = NtQueryInformationProcess(
        GetCurrentProcess(),
        ProcessDebugPort,
        &debug_port,
        sizeof(debug_port),
        NULL
    );
    
    if (NT_SUCCESS(status) && debug_port != 0) {
        return TRUE;
    }
    
    ULONG debug_flags = 0;
    status = NtQueryInformationProcess(
        GetCurrentProcess(),
        ProcessDebugFlags,
        &debug_flags,
        sizeof(debug_flags),
        NULL
    );
    
    if (NT_SUCCESS(status) && debug_flags == 0) {
        return TRUE;
    }
    
    return FALSE;
}

int main() {
    printf("[LAB-9] Level 7: Kernel-Level Anti-Debug\n");
    printf("[*] Checking kernel-level debugger presence...\n");
    
    if (!IsDebuggerPresent()) {
        printf("[!] IsDebuggerPresent detected no debugger!\n");
        return 1;
    }
    
    if (check_kernel_debug()) {
        printf("[!] Kernel-level debugger detected!\n");
        printf("[!] Try to bypass kernel-level detection.\n");
        return 1;
    }
    
    printf("[+] No kernel-level debugger detected!\n");
    printf("[+] Congratulations! You've bypassed kernel-level detection.\n");
    printf("[+] Flag: %s\n", generate_flag(7));
    
    system("pause");
    return 0;
} 