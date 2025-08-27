# LAB-9 v1.0.0 – level=1,technique=IsDebuggerPresent,author=Lethe
# Ghidra script to automatically patch level_01.exe

from ghidra.app.decompiler import DecompInterface
from ghidra.program.model.symbol import SymbolType

# #region LAB-9:level=1,technique=IsDebuggerPresent,status=automated

def find_and_patch_isdebuggerpresent():
    """
    Find IsDebuggerPresent call and patch the test instruction
    """
    print("[LAB-9] Level 1: Automated IsDebuggerPresent bypass")
    
    # Find IsDebuggerPresent symbol
    symbol_table = currentProgram.getSymbolTable()
    isdebugger_symbol = symbol_table.getSymbol("IsDebuggerPresent", None)
    
    if not isdebugger_symbol:
        print("[!] IsDebuggerPresent symbol not found!")
        return False
    
    # Get references to IsDebuggerPresent
    refs = getReferencesTo(isdebugger_symbol.getAddress())
    
    for ref in refs:
        if ref.getReferenceType().isCall():
            call_addr = ref.getFromAddress()
            print(f"[+] Found IsDebuggerPresent call at {call_addr}")
            
            # Find the test instruction after the call
            test_addr = find_test_instruction_after_call(call_addr)
            if test_addr:
                patch_test_instruction(test_addr)
                return True
    
    return False

def find_test_instruction_after_call(call_addr):
    """
    Find test eax,eax instruction after IsDebuggerPresent call
    """
    # Look for test eax,eax (85 C0) within 20 bytes after call
    for i in range(1, 20):
        addr = call_addr.add(i)
        if addr >= currentProgram.getMaxAddress():
            break
            
        try:
            instr = getInstructionAt(addr)
            if instr and instr.getMnemonicString() == "TEST":
                op1 = instr.getOpObjects(0)[0]
                op2 = instr.getOpObjects(1)[0]
                if str(op1) == "EAX" and str(op2) == "EAX":
                    print(f"[+] Found test eax,eax at {addr}")
                    return addr
        except:
            continue
    
    return None

def patch_test_instruction(test_addr):
    """
    Patch test eax,eax -> xor eax,eax
    """
    try:
        # Create patch: 85 C0 -> 31 C0
        patch_bytes = [0x31, 0xC0]  # xor eax,eax
        
        # Apply patch
        for i, byte in enumerate(patch_bytes):
            addr = test_addr.add(i)
            setByte(addr, byte)
        
        print(f"[+] Patched test instruction at {test_addr}")
        print("[+] IsDebuggerPresent bypass successful!")
        print("[+] Flag: flag{b4by_st3ps_1337}")
        
    except Exception as e:
        print(f"[!] Patch failed: {e}")

# Main execution
if __name__ == "__main__":
    if find_and_patch_isdebuggerpresent():
        print("[+] Level 1 bypass completed successfully!")
    else:
        print("[!] Failed to find or patch IsDebuggerPresent check")

# #endregion 