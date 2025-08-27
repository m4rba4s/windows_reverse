# LAB-9 Quick Test Guide
## Pre-Posting Verification Checklist

**Author:** Lethe  
**Purpose:** Verify all functionality before Git push  
**Time Required:** 10-15 minutes

---

## 🚀 **Quick Test Sequence**

### 1. **Build System Test**
```bash
# Test build system
python LAB-9/tools/build.py

# Expected: All 9 levels built successfully
# Check: bin/ folder contains all .exe files
```

### 2. **No Debugger Test**
```bash
# Test that levels fail without debugger
python LAB-9/tests/test_no_dbg.py

# Expected: All 9 levels PASS (exit code 1)
# This proves Zero-Accident Design works
```

### 3. **Partial Patch Test**
```bash
# Test partial patch protection
python LAB-9/tests/test_partial_patch.py

# Expected: All 9 levels PASS (exit code 1)
# This proves protection against incomplete patches
```

### 4. **Manual Level Test**
```bash
# Test one level manually
.\bin\level_01.exe

# Expected: "No debugger detected! Access denied."
# Exit code: 1
```

### 5. **File Structure Check**
```bash
# Verify all required files exist
dir LAB-9
dir LAB-9\bin
dir LAB-9\levels
dir LAB-9\tools
dir LAB-9\tests
```

**Expected Files:**
- `README.md` ✅
- `ARCHITECTURE.md` ✅
- `WALKTHROUGH.md` ✅
- `QUICK_TEST.md` ✅
- `requirements.txt` ✅
- `LICENSE` ✅
- `.gitignore` ✅
- `bin/level_01.exe` through `bin/level_09.exe` ✅
- `bin/manifest.json` ✅
- `bin/sha256sums.txt` ✅

---

## 🔍 **Detailed Verification**

### **Level 1 Test (Basic)**
1. Run `.\bin\level_01.exe` → Should fail
2. Load in x64dbg → Should show anti-debug message
3. Patch `IsDebuggerPresent` → Should show flag

### **Level 6 Test (VM)**
1. Run `.\bin\level_06.exe` → Should fail
2. Check for timeout issues → Should complete within 5 seconds
3. Verify VM bytecode is working

### **Level 9 Test (Final)**
1. Run `.\bin\level_09.exe` → Should fail
2. Check all anti-debug techniques are present
3. Verify complexity is appropriate

---

## ⚠️ **Common Issues to Check**

### **Build Issues**
- [ ] All levels compile without errors
- [ ] No missing dependencies
- [ ] Hardening flags applied correctly

### **Runtime Issues**
- [ ] No infinite loops
- [ ] No crashes on startup
- [ ] Proper error messages displayed

### **Security Issues**
- [ ] No accidental bypasses
- [ ] Dynamic flag generation working
- [ ] Anti-debug checks functional

### **Documentation Issues**
- [ ] README.md is complete
- [ ] WALKTHROUGH.md is accurate
- [ ] All paths are correct

---

## 🎯 **Success Criteria**

### **Must Pass:**
- [ ] All 9 levels build successfully
- [ ] All tests pass (no debugger, partial patch)
- [ ] No accidental bypasses possible
- [ ] Dynamic flags generate correctly
- [ ] Documentation is complete

### **Nice to Have:**
- [ ] CLI tool works (labctl.py)
- [ ] CI/CD pipeline ready
- [ ] All walkthroughs tested manually

---

## 🚨 **If Issues Found**

### **Build Failures:**
1. Check compiler installation
2. Verify source code syntax
3. Check file paths

### **Test Failures:**
1. Review anti-debug logic
2. Check exit codes
3. Verify test expectations

### **Runtime Crashes:**
1. Check for missing dependencies
2. Review memory management
3. Test on clean system

---

## ✅ **Final Checklist**

Before pushing to Git:

- [ ] **Build System:** All levels compile ✅
- [ ] **Testing:** All automated tests pass ✅
- [ ] **Security:** No accidental bypasses ✅
- [ ] **Documentation:** Complete and accurate ✅
- [ ] **File Structure:** All files present ✅
- [ ] **Git Ready:** .gitignore and LICENSE present ✅

---

## 🎉 **Ready to Push!**

If all checks pass, your LAB-9 is ready for:
- Git push
- Public release
- Training use
- CTF challenges

**Congratulations! You've built a professional-grade reverse engineering training lab!**

---

*This quick test guide ensures LAB-9 meets production standards before release.* 