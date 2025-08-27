#include <windows.h>
#include <stdio.h>

unsigned char vm_code[] = {
    0x01, 0x00, 0x05, 0x09, 0x00, 0x00, 0x0A, 0x00, 0x08, 0x00
};

char* generate_flag(int level) {
    static char flag[64];
    DWORD seed = GetTickCount() ^ 0xDEADBEEF;
    sprintf(flag, "flag{level_%d_%08x}", level, seed);
    return flag;
}

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

int main() {
    printf("[LAB-9] Level 6: VM Protection\n");
    printf("[*] Executing custom VM with anti-debug...\n");
    
    int result = vm_execute(vm_code, sizeof(vm_code));
    
    if (result == 1) {
        printf("[!] VM detected no debugger!\n");
        printf("[!] Try to reverse the VM and bypass its checks.\n");
        return 1;
    }
    
    printf("[+] VM execution completed successfully!\n");
    printf("[+] Congratulations! You've reversed the VM protection.\n");
    printf("[+] Flag: %s\n", generate_flag(6));
    
    system("pause");
    return 0;
} 