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

#ifndef NT_SUCCESS
#define NT_SUCCESS(Status) (((NTSTATUS)(Status)) >= 0)
#endif

unsigned char vm_bytecode[] = {
    0x09, 0x00, 0x00, 0x0A, 0x00, 0x08, 0x01, 0x01, 0x32, 0x0C, 0x01, 0x00, 0x01, 0x00, 0x00, 0x08,
    0x00
};

int vm_execute(unsigned char* code, int len) {
    int reg[4] = {0};
    int pc = 0;
    
    while (pc < len) {
        unsigned char opcode = code[pc++];
        unsigned char op1 = code[pc++];
        unsigned char op2 = code[pc++];
        
        switch (opcode) {
            case 0x01: reg[op1] = op2; break;
            case 0x02: reg[op1] += reg[op2]; break;
            case 0x03: reg[op1] -= reg[op2]; break;
            case 0x04: reg[op1] *= reg[op2]; break;
            case 0x05: reg[op1] ^= reg[op2]; break;
            case 0x06: if (reg[op1] == reg[op2]) pc += 3; break;
            case 0x07: if (reg[op1] != reg[op2]) pc += 3; break;
            case 0x08: return reg[op1];
            case 0x09: reg[op1] = IsDebuggerPresent(); break;
            case 0x0A: if (!reg[op1]) return 1; break;
            case 0x0B: reg[op1] = GetTickCount(); break;
            case 0x0C: Sleep(reg[op1]); break;
        }
    }
    return 0;
}

BOOL check_kernel_debug() {
    HMODULE ntdll = GetModuleHandleA("ntdll.dll");
    if (!ntdll) return TRUE;
    
    NtQueryInformationProcess_t NtQueryInformationProcess = 
        (NtQueryInformationProcess_t)GetProcAddress(ntdll, "NtQueryInformationProcess");
    if (!NtQueryInformationProcess) return TRUE;
    
    ULONG debug_port = 0;
    NTSTATUS status = NtQueryInformationProcess(
        GetCurrentProcess(),
        7,
        &debug_port,
        sizeof(debug_port),
        NULL
    );
    
    if (NT_SUCCESS(status) && debug_port != 0) return TRUE;
    
    ULONG debug_flags = 0;
    status = NtQueryInformationProcess(
        GetCurrentProcess(),
        31,
        &debug_flags,
        sizeof(debug_flags),
        NULL
    );
    
    if (NT_SUCCESS(status) && debug_flags == 0) return TRUE;
    
    return FALSE;
}

BOOL check_hardware_breakpoints() {
    CONTEXT ctx;
    ctx.ContextFlags = CONTEXT_DEBUG_REGISTERS;
    
    if (!GetThreadContext(GetCurrentThread(), &ctx)) return TRUE;
    
    if (ctx.Dr0 != 0 || ctx.Dr1 != 0 || ctx.Dr2 != 0 || ctx.Dr3 != 0) return TRUE;
    
    return FALSE;
}

int main() {
    printf("[LAB-9] Level 9: Final Boss\n");
    printf("[*] All anti-debug techniques combined...\n");
    
    DWORD start_time = GetTickCount();
    
    if (!IsDebuggerPresent()) {
        printf("[!] IsDebuggerPresent detected no debugger!\n");
        return 1;
    }
    
    if (check_kernel_debug()) {
        printf("[!] Kernel-level debugger detected!\n");
        return 1;
    }
    
    if (check_hardware_breakpoints()) {
        printf("[!] Hardware breakpoints detected!\n");
        return 1;
    }
    
    int vm_result = vm_execute(vm_bytecode, sizeof(vm_bytecode));
    if (vm_result == 1) {
        printf("[!] VM detected no debugger!\n");
        return 1;
    }
    
    DWORD end_time = GetTickCount();
    if ((end_time - start_time) > 500) {
        printf("[!] Timing check failed!\n");
        return 1;
    }
    
    printf("[+] All checks bypassed successfully!\n");
    printf("[+] You are a master reverse engineer!\n");
    printf("[+] Flag: %s\n", generate_flag(9));
    
    system("pause");
    return 0;
} 