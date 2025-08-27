# LAB-9 Reverse Engineering Walkthrough
## Complete Step-by-Step Guide

**Author:** Lethe  
**Version:** 2.1  
**Difficulty:** Progressive (Level 1-9)  
**Tools Required:** x64dbg, Ghidra, Cheat Engine, ScyllaHide

---

## 🎯 **Level 1: Baby Steps**
**Technique:** IsDebuggerPresent() Bypass  
**Difficulty:** ⭐  
**Expected Time:** 5-10 minutes

### Tools
- x64dbg
- ScyllaHide (optional)

### Step-by-Step

#### Step 1: Initial Analysis
```bash
# Run the executable
.\bin\level_01.exe
```
**Expected Output:**
```
[LAB-9] Level 1: Baby Steps
[*] Checking for debugger...
[!] No debugger detected! Access denied.
[!] Try to bypass this check by patching.
```

#### Step 2: Load in x64dbg
1. Open x64dbg
2. File → Open → `level_01.exe`
3. Press F9 to run

#### Step 3: Find the Check
1. Press Ctrl+G (Go to)
2. Type: `kernel32!IsDebuggerPresent`
3. Press Enter
4. Set breakpoint on the function (F2)

#### Step 4: Analyze the Logic
1. Run the program (F9)
2. When it hits the breakpoint, step out (Ctrl+F9)
3. You'll see something like:
```assembly
call kernel32!IsDebuggerPresent
test eax,eax
jz short 0x401234  ; Jump if debugger not present
```

#### Step 5: Patch the Check
**Option A: Patch the jump**
1. Find the `jz` instruction
2. Right-click → Binary → Fill with NOPs
3. Or change `jz` to `jmp` (74 → EB)

**Option B: Patch the return value**
1. Go back to IsDebuggerPresent call
2. After the call, patch `test eax,eax` to `xor eax,eax`
3. This makes the function always return 0 (no debugger)

#### Step 6: Verify the Patch
1. Run the program (F9)
2. **Expected Output:**
```
[LAB-9] Level 1: Baby Steps
[*] Checking for debugger...
[+] Debugger detected!
[+] Congratulations! You've bypassed the check.
[+] Flag: flag{level_1_XXXXXXXX}
```

### x64dbg Patch File
```1337
level_01.exe
0x401234: 74 12 -> 90 90  ; NOP out the jump
```

---

## 🎯 **Level 2: Multi-Check**
**Technique:** Multiple Anti-Debug Checks  
**Difficulty:** ⭐⭐  
**Expected Time:** 10-15 minutes

### Tools
- x64dbg
- ScyllaHide

### Step-by-Step

#### Step 1: Initial Analysis
```bash
.\bin\level_02.exe
```
**Expected Output:**
```
[LAB-9] Level 2: Multi-Check
[*] Running multiple anti-debug checks...
[!] Check 1 failed: IsDebuggerPresent
[!] Check 2 failed: CheckRemoteDebuggerPresent
[!] Access denied.
```

#### Step 2: Load in x64dbg
1. Open x64dbg
2. Load `level_02.exe`
3. Run (F9)

#### Step 3: Find All Checks
1. Search for strings: "Check 1 failed"
2. Look for multiple calls to:
   - `IsDebuggerPresent`
   - `CheckRemoteDebuggerPresent`

#### Step 4: Patch Both Checks
**Method 1: Patch return values**
```assembly
; After IsDebuggerPresent call
mov eax,0    ; Force return 0

; After CheckRemoteDebuggerPresent call  
mov eax,0    ; Force return 0
```

**Method 2: Use ScyllaHide**
1. Enable ScyllaHide plugin
2. Check "IsDebuggerPresent"
3. Check "CheckRemoteDebuggerPresent"
4. Apply patches

#### Step 5: Verify
**Expected Output:**
```
[LAB-9] Level 2: Multi-Check
[*] Running multiple anti-debug checks...
[+] Check 1 passed: IsDebuggerPresent
[+] Check 2 passed: CheckRemoteDebuggerPresent
[+] All checks bypassed!
[+] Flag: flag{level_2_XXXXXXXX}
```

### x64dbg Patch File
```1337
level_02.exe
0x401245: 85 C0 -> 31 C0  ; test eax,eax -> xor eax,eax
0x401256: 85 C0 -> 31 C0  ; test eax,eax -> xor eax,eax
```

---

## 🎯 **Level 3: Packed Protection**
**Technique:** UPX Packing + Anti-Debug  
**Difficulty:** ⭐⭐⭐  
**Expected Time:** 15-20 minutes

### Tools
- x64dbg
- UPX (for unpacking)
- PE Explorer (optional)

### Step-by-Step

#### Step 1: Detect Packing
```bash
# Check if packed
strings bin\level_03.exe | findstr UPX
```
**Expected:** UPX strings found

#### Step 2: Unpack
**Option A: Manual unpacking**
1. Load in x64dbg
2. Run until you hit the OEP (Original Entry Point)
3. Look for UPX stub
4. Find the jump to original code
5. Dump the process

**Option B: UPX tool**
```bash
upx -d bin\level_03.exe
```

#### Step 3: Analyze Unpacked Code
1. Load the unpacked executable
2. Look for anti-debug checks
3. Find the main logic

#### Step 4: Patch Anti-Debug
Similar to Level 1-2, but in unpacked code

#### Step 5: Verify
**Expected Output:**
```
[LAB-9] Level 3: Packed Protection
[*] Unpacking and checking...
[+] Successfully unpacked!
[+] Anti-debug bypassed!
[+] Flag: flag{level_3_XXXXXXXX}
```

---

## 🎯 **Level 4: Timing Attack**
**Technique:** Timing-Based Anti-Debug  
**Difficulty:** ⭐⭐⭐  
**Expected Time:** 20-25 minutes

### Tools
- x64dbg
- Process Monitor
- API Monitor

### Step-by-Step

#### Step 1: Initial Analysis
```bash
.\bin\level_04.exe
```
**Expected Output:**
```
[LAB-9] Level 4: Timing Attack
[*] Running timing checks...
[!] Timing check failed - debugger detected!
```

#### Step 2: Monitor API Calls
1. Use API Monitor or Process Monitor
2. Look for timing-related APIs:
   - `GetTickCount`
   - `QueryPerformanceCounter`
   - `RDTSC`

#### Step 3: Find Timing Logic
1. Load in x64dbg
2. Search for timing functions
3. Look for code like:
```assembly
call GetTickCount
mov [esp+4], eax
call Sleep
call GetTickCount
sub eax, [esp+4]
cmp eax, 1000  ; Check if sleep was bypassed
```

#### Step 4: Patch Timing Check
**Method 1: Patch the comparison**
```assembly
; Change the timing comparison
cmp eax, 1000
jg short 0x401234  ; Jump if greater
; To:
nop
nop
nop
nop
```

**Method 2: Hook Sleep function**
1. Find Sleep call
2. Replace with NOPs
3. Or modify the timing calculation

#### Step 5: Verify
**Expected Output:**
```
[LAB-9] Level 4: Timing Attack
[*] Running timing checks...
[+] Timing check passed!
[+] Flag: flag{level_4_XXXXXXXX}
```

---

## 🎯 **Level 5: API Hooking Detection**
**Technique:** API Hook Detection  
**Difficulty:** ⭐⭐⭐⭐  
**Expected Time:** 25-30 minutes

### Tools
- x64dbg
- API Monitor
- ScyllaHide

### Step-by-Step

#### Step 1: Initial Analysis
```bash
.\bin\level_05.exe
```
**Expected Output:**
```
[LAB-9] Level 5: API Hooking Detection
[*] Checking for API hooks...
[!] Hook detected on NtQueryInformationProcess!
[!] Hint: restore prologue at 0x7FFE12345678
```

#### Step 2: Understand Hook Detection
The program checks if API functions have been hooked by:
1. Reading the first few bytes of the function
2. Comparing with expected values
3. Detecting if they've been modified

#### Step 3: Find Hook Detection Code
1. Load in x64dbg
2. Search for "Hook detected"
3. Look for code that:
   - Gets function address
   - Reads function bytes
   - Compares with expected values

#### Step 4: Bypass Hook Detection
**Method 1: Patch the detection**
```assembly
; Find the comparison
cmp eax, expected_value
jz short hook_detected
; Change to:
nop
nop
nop
nop
```

**Method 2: Restore original bytes**
1. Use the hint address provided
2. Restore original function prologue
3. Or patch the detection logic

#### Step 5: Verify
**Expected Output:**
```
[LAB-9] Level 5: API Hooking Detection
[*] Checking for API hooks...
[+] No hooks detected!
[+] Flag: flag{level_5_XXXXXXXX}
```

---

## 🎯 **Level 6: Custom VM**
**Technique:** Custom Bytecode Interpreter  
**Difficulty:** ⭐⭐⭐⭐⭐  
**Expected Time:** 30-45 minutes

### Tools
- x64dbg
- Ghidra
- Python (for bytecode analysis)

### Step-by-Step

#### Step 1: Initial Analysis
```bash
.\bin\level_06.exe
```
**Expected Output:**
```
[LAB-9] Level 6: Custom VM
[*] Initializing virtual machine...
[!] VM execution failed!
```

#### Step 2: Analyze VM Structure
1. Load in Ghidra
2. Look for:
   - Bytecode array
   - VM interpreter loop
   - Instruction handlers

#### Step 3: Understand Bytecode
The VM likely has:
- Custom instruction set
- Stack-based operations
- Anti-debug checks in bytecode

#### Step 4: Reverse Engineer Bytecode
1. Find the bytecode array
2. Analyze instruction format
3. Understand what each instruction does
4. Look for the flag generation logic

#### Step 5: Patch VM or Bytecode
**Method 1: Patch VM logic**
- Find the main VM loop
- Modify instruction handlers
- Bypass anti-debug checks

**Method 2: Modify bytecode**
- Find the bytecode array
- Modify specific instructions
- Change the execution flow

#### Step 6: Verify
**Expected Output:**
```
[LAB-9] Level 6: Custom VM
[*] Initializing virtual machine...
[+] VM execution successful!
[+] Flag: flag{level_6_XXXXXXXX}
```

---

## 🎯 **Level 7: Kernel-Level**
**Technique:** Kernel Anti-Debug  
**Difficulty:** ⭐⭐⭐⭐⭐  
**Expected Time:** 45-60 minutes

### Tools
- x64dbg
- WinDbg (kernel debugger)
- Process Monitor

### Step-by-Step

#### Step 1: Initial Analysis
```bash
.\bin\level_07.exe
```
**Expected Output:**
```
[LAB-9] Level 7: Kernel-Level
[*] Checking kernel-level anti-debug...
[!] Kernel check failed!
```

#### Step 2: Understand Kernel Checks
This level likely uses:
- `NtQueryInformationProcess` with `ProcessDebugPort`
- `NtQuerySystemInformation`
- Direct kernel calls

#### Step 3: Monitor System Calls
1. Use Process Monitor
2. Look for system calls
3. Identify which ones are being checked

#### Step 4: Bypass Kernel Checks
**Method 1: Hook system calls**
1. Find the system call functions
2. Hook them to return false
3. Or patch the return values

**Method 2: Use kernel debugger**
1. Use WinDbg
2. Set breakpoints on kernel functions
3. Modify kernel behavior

#### Step 5: Verify
**Expected Output:**
```
[LAB-9] Level 7: Kernel-Level
[*] Checking kernel-level anti-debug...
[+] Kernel checks passed!
[+] Flag: flag{level_7_XXXXXXXX}
```

---

## 🎯 **Level 8: Hardware Breakpoints**
**Technique:** Hardware Breakpoint Detection  
**Difficulty:** ⭐⭐⭐⭐⭐  
**Expected Time:** 30-40 minutes

### Tools
- x64dbg
- ScyllaHide
- Custom debugger

### Step-by-Step

#### Step 1: Initial Analysis
```bash
.\bin\level_08.exe
```
**Expected Output:**
```
[LAB-9] Level 8: Hardware Breakpoints
[*] Checking for hardware breakpoints...
[!] Hardware breakpoint detected!
```

#### Step 2: Understand Hardware Breakpoints
The program checks:
- Debug registers (DR0-DR7)
- Hardware breakpoint flags
- Exception handlers

#### Step 3: Find Detection Code
1. Load in x64dbg
2. Search for debug register access
3. Look for `mov` instructions to/from DR registers

#### Step 4: Bypass Detection
**Method 1: Clear debug registers**
```assembly
; Clear all debug registers
xor eax, eax
mov dr0, eax
mov dr1, eax
mov dr2, eax
mov dr3, eax
```

**Method 2: Patch detection**
- Find the debug register checks
- Patch the comparison logic
- Or hook the detection function

#### Step 5: Verify
**Expected Output:**
```
[LAB-9] Level 8: Hardware Breakpoints
[*] Checking for hardware breakpoints...
[+] No hardware breakpoints detected!
[+] Flag: flag{level_8_XXXXXXXX}
```

---

## 🎯 **Level 9: Final Challenge**
**Technique:** Combined All Techniques  
**Difficulty:** ⭐⭐⭐⭐⭐  
**Expected Time:** 60-90 minutes

### Tools
- All previous tools
- Custom scripts
- Advanced techniques

### Step-by-Step

#### Step 1: Initial Analysis
```bash
.\bin\level_09.exe
```
**Expected Output:**
```
[LAB-9] Level 9: Final Challenge
[*] Running comprehensive checks...
[!] Multiple checks failed!
[!] This is the ultimate challenge!
```

#### Step 2: Comprehensive Analysis
This level combines:
- All previous anti-debug techniques
- Custom VM
- Kernel-level checks
- Hardware breakpoint detection
- State validation

#### Step 3: Systematic Approach
1. **Identify all checks**
   - Use Process Monitor
   - API Monitor
   - Dynamic analysis

2. **Prioritize by difficulty**
   - Start with simple checks
   - Work up to complex ones

3. **Apply previous techniques**
   - Use solutions from levels 1-8
   - Combine multiple approaches

#### Step 4: Advanced Techniques
**Method 1: Multi-stage patching**
1. Patch each check individually
2. Test after each patch
3. Ensure no conflicts

**Method 2: Custom debugger**
1. Write custom debugger
2. Handle all anti-debug techniques
3. Provide clean execution environment

#### Step 5: Verify
**Expected Output:**
```
[LAB-9] Level 9: Final Challenge
[*] Running comprehensive checks...
[+] All checks passed!
[+] Congratulations! You've mastered LAB-9!
[+] Final Flag: flag{level_9_XXXXXXXX}
```

---

## 🛠️ **General Tips & Tricks**

### Common Anti-Debug Techniques
1. **IsDebuggerPresent()** - Basic check
2. **CheckRemoteDebuggerPresent()** - Remote debugger check
3. **NtQueryInformationProcess()** - Kernel-level check
4. **Timing checks** - Detect debugger slowdown
5. **API hooking detection** - Find modified APIs
6. **Hardware breakpoints** - Check debug registers
7. **Custom VM** - Interpreted code
8. **Packing/obfuscation** - Hide real code

### Tools Overview
- **x64dbg** - Primary debugger
- **Ghidra** - Static analysis
- **ScyllaHide** - Anti-anti-debug
- **Process Monitor** - System call monitoring
- **API Monitor** - API call tracking
- **Cheat Engine** - Memory patching

### Patching Techniques
1. **NOP out jumps** - Remove conditional logic
2. **Change comparisons** - Modify check results
3. **Hook functions** - Intercept API calls
4. **Modify return values** - Force specific results
5. **Patch bytecode** - Modify interpreted code

### Verification Checklist
- [ ] Program runs without errors
- [ ] Flag is displayed correctly
- [ ] No crashes or timeouts
- [ ] All anti-debug bypassed
- [ ] Solution is repeatable

---

## 🎉 **Congratulations!**

If you've completed all 9 levels, you've mastered:
- Basic anti-debug bypass
- Advanced reverse engineering
- Custom VM analysis
- Kernel-level debugging
- Hardware breakpoint handling
- Comprehensive security analysis

**You're now ready for real-world reverse engineering challenges!**

---

*This walkthrough is part of LAB-9 Reverse Engineering Training Lab v2.1* 