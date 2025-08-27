# LAB-9 Reverse Engineering Training Lab
## Professional Anti-Debug Challenge Suite

**Author:** Lethe  
**Version:** 2.1 "Reality-Hardened"  
**Difficulty:** Progressive (Beginner to Expert)  
**Platform:** Windows x64  
**License:** MIT

---

## 🎯 **Overview**

LAB-9 is a comprehensive reverse engineering training lab featuring 9 progressively difficult levels that teach anti-debug bypass techniques. Each level introduces new challenges, from basic API checks to advanced kernel-level anti-debug mechanisms.

**Perfect for:**
- Reverse engineering beginners
- Security researchers
- CTF participants
- Malware analysts
- Red team training

---

## 🚀 **Quick Start**

### Prerequisites
- Windows 10/11 (x64)
- x64dbg or x32dbg
- Ghidra (optional)
- Python 3.7+ (for build tools)

### Installation
```bash
# Clone the repository
git clone https://github.com/your-repo/LAB-9.git
cd LAB-9

# Install dependencies
pip install -r requirements.txt

# Build all levels
python tools/build.py

# Test that everything works
python tests/test_no_dbg.py
```

### First Level
```bash
# Run the first level
.\bin\level_01.exe

# Expected output:
[LAB-9] Level 1: Baby Steps
[*] Checking for debugger...
[!] No debugger detected! Access denied.
[!] Try to bypass this check by patching.
```

---

## 📚 **Level Descriptions**

### **Level 1: Baby Steps** ⭐
**Technique:** `IsDebuggerPresent()` Bypass  
**Time:** 5-10 minutes  
**Skills:** Basic patching, x64dbg usage

**Challenge:** The program checks if a debugger is present using the Windows API. If no debugger is detected, it fails.

**Learning Objectives:**
- Understanding basic anti-debug techniques
- Using x64dbg for dynamic analysis
- Patching conditional jumps
- Understanding assembly code flow

**Tools Needed:**
- x64dbg
- Basic assembly knowledge

---

### **Level 2: Multi-Check** ⭐⭐
**Technique:** Multiple Anti-Debug Checks  
**Time:** 10-15 minutes  
**Skills:** Multiple API bypass, systematic approach

**Challenge:** The program performs multiple anti-debug checks using different Windows APIs.

**Learning Objectives:**
- Handling multiple anti-debug checks
- Systematic patching approach
- Understanding different Windows APIs
- Using ScyllaHide plugin

**Tools Needed:**
- x64dbg
- ScyllaHide (optional)
- Process Monitor

---

### **Level 3: Packed Protection** ⭐⭐⭐
**Technique:** UPX Packing + Anti-Debug  
**Time:** 15-20 minutes  
**Skills:** Unpacking, post-unpack analysis

**Challenge:** The executable is packed with UPX, hiding the real anti-debug code.

**Learning Objectives:**
- Detecting packed executables
- Manual and automated unpacking
- Post-unpack analysis
- Understanding packer stubs

**Tools Needed:**
- x64dbg
- UPX tool
- PE Explorer (optional)

---

### **Level 4: Timing Attack** ⭐⭐⭐
**Technique:** Timing-Based Anti-Debug  
**Time:** 20-25 minutes  
**Skills:** Timing analysis, API monitoring

**Challenge:** The program uses timing checks to detect if debugging operations have been bypassed.

**Learning Objectives:**
- Understanding timing-based anti-debug
- Using API monitoring tools
- Patching timing comparisons
- Real-time analysis

**Tools Needed:**
- x64dbg
- Process Monitor
- API Monitor

---

### **Level 5: API Hooking Detection** ⭐⭐⭐⭐
**Technique:** API Hook Detection  
**Time:** 25-30 minutes  
**Skills:** Hook detection, function analysis

**Challenge:** The program detects if API functions have been hooked by examining their prologue bytes.

**Learning Objectives:**
- Understanding API hooking
- Function prologue analysis
- Bypassing hook detection
- Advanced patching techniques

**Tools Needed:**
- x64dbg
- API Monitor
- ScyllaHide

---

### **Level 6: Custom VM** ⭐⭐⭐⭐⭐
**Technique:** Custom Bytecode Interpreter  
**Time:** 30-45 minutes  
**Skills:** VM analysis, bytecode reverse engineering

**Challenge:** The program uses a custom virtual machine with anti-debug checks embedded in the bytecode.

**Learning Objectives:**
- Understanding custom VMs
- Bytecode analysis
- VM interpreter reverse engineering
- Advanced debugging techniques

**Tools Needed:**
- x64dbg
- Ghidra
- Python (for analysis)

---

### **Level 7: Kernel-Level** ⭐⭐⭐⭐⭐
**Technique:** Kernel Anti-Debug  
**Time:** 45-60 minutes  
**Skills:** Kernel-level analysis, system calls

**Challenge:** The program uses kernel-level APIs to detect debugging at the system level.

**Learning Objectives:**
- Understanding kernel-level anti-debug
- System call analysis
- Kernel API usage
- Advanced bypass techniques

**Tools Needed:**
- x64dbg
- WinDbg (optional)
- Process Monitor

---

### **Level 8: Hardware Breakpoints** ⭐⭐⭐⭐⭐
**Technique:** Hardware Breakpoint Detection  
**Time:** 30-40 minutes  
**Skills:** Debug registers, hardware analysis

**Challenge:** The program checks debug registers to detect hardware breakpoints.

**Learning Objectives:**
- Understanding debug registers
- Hardware breakpoint detection
- Register manipulation
- Low-level debugging

**Tools Needed:**
- x64dbg
- ScyllaHide
- Custom debugger (optional)

---

### **Level 9: Final Challenge** ⭐⭐⭐⭐⭐
**Technique:** Combined All Techniques  
**Time:** 60-90 minutes  
**Skills:** Comprehensive analysis, systematic approach

**Challenge:** Combines all previous techniques plus additional complexity and state validation.

**Learning Objectives:**
- Systematic problem-solving
- Combining multiple techniques
- Advanced reverse engineering
- Real-world scenario simulation

**Tools Needed:**
- All previous tools
- Custom scripts
- Advanced techniques

---

## 🛠️ **Tools & Resources**

### Essential Tools
- **x64dbg/x32dbg** - Primary debugger
- **Ghidra** - Static analysis
- **Process Monitor** - System call monitoring
- **API Monitor** - API call tracking

### Optional Tools
- **ScyllaHide** - Anti-anti-debug plugin
- **Cheat Engine** - Memory patching
- **PE Explorer** - PE file analysis
- **UPX** - Packer tool

### Learning Resources
- [x64dbg Documentation](https://x64dbg.com/)
- [Ghidra User Guide](https://ghidra-sre.org/)
- [Windows API Documentation](https://docs.microsoft.com/en-us/windows/win32/api/)
- [Assembly Language Reference](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html)

---

## 📖 **Documentation**

### Architecture
See `ARCHITECTURE.md` for detailed technical architecture and design principles.

### Walkthrough
See `WALKTHROUGH.md` for step-by-step solutions to all levels.

### Quick Test
See `QUICK_TEST.md` for pre-posting verification checklist.

---

## 🔧 **Build System**

### Automated Build
```bash
# Build all levels
python tools/build.py

# Build specific level
python tools/build.py --level 5

# Clean build artifacts
python tools/clean.py
```

### Manual Build
```bash
# Compile individual level
x86_64-w64-mingw32-gcc -O2 -static -s levels/level_01/level_01.c -o bin/level_01.exe
```

### Build Verification
```bash
# Test no-debugger protection
python tests/test_no_dbg.py

# Test partial patch protection
python tests/test_partial_patch.py
```

---

## 🎓 **Learning Path**

### Beginner Track (Levels 1-3)
1. **Level 1:** Learn basic debugging and patching
2. **Level 2:** Handle multiple checks systematically
3. **Level 3:** Understand packing and unpacking

### Intermediate Track (Levels 4-6)
4. **Level 4:** Master timing-based analysis
5. **Level 5:** Learn API hooking and detection
6. **Level 6:** Understand custom VMs and bytecode

### Advanced Track (Levels 7-9)
7. **Level 7:** Kernel-level debugging
8. **Level 8:** Hardware-level analysis
9. **Level 9:** Comprehensive challenge

---

## 🏆 **Success Criteria**

### For Each Level
- [ ] Program runs without crashes
- [ ] Flag is displayed correctly
- [ ] Anti-debug bypass is complete
- [ ] Solution is repeatable
- [ ] Understanding of technique demonstrated

### Overall Mastery
- [ ] All 9 levels completed
- [ ] Understanding of all anti-debug techniques
- [ ] Ability to apply techniques to real malware
- [ ] Comfort with advanced debugging tools
- [ ] Systematic problem-solving approach

---

## 🤝 **Contributing**

### Reporting Issues
- Use GitHub Issues for bug reports
- Include detailed reproduction steps
- Attach relevant files and logs

### Suggesting Improvements
- Open GitHub Discussions for ideas
- Submit pull requests for enhancements
- Help improve documentation

### Adding Levels
- Follow the existing architecture
- Include comprehensive tests
- Update documentation
- Ensure Zero-Accident Design compliance

---

## 📄 **License**

This project is licensed under the MIT License - see the `LICENSE` file for details.

---

## 🙏 **Acknowledgments**

- **x64dbg Team** - Excellent debugging platform
- **Ghidra Team** - Powerful reverse engineering tool
- **UPX Team** - Packer tool
- **Reverse Engineering Community** - Continuous inspiration

---

## 📞 **Support**

- **Documentation:** Check the docs folder
- **Issues:** GitHub Issues
- **Discussions:** GitHub Discussions
- **Email:** [your-email@domain.com]

---

*LAB-9: Where reverse engineering meets reality.* 