#!/usr/bin/env python3
# LAB-9 v2.1 - Deterministic Build System
# Author: Lethe

import os, hashlib, subprocess, json, pathlib, sys
from typing import Dict, Any

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

MANIFEST = {
    "version": "2.1",
    "architecture": "Reality-Hardened",
    "levels": {}
}

def calculate_hash(filepath: str) -> str:
    """Calculate SHA256 hash of file"""
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def build_level(level_num: int) -> Dict[str, Any]:
    """Build single level with hardening"""
    src = os.path.join(PROJECT_ROOT, f"levels/level_{level_num:02d}/level_{level_num:02d}.c")
    dst = os.path.join(PROJECT_ROOT, f"bin/level_{level_num:02d}.exe")
    
    if not os.path.exists(src):
        print(f"[!] Source file not found: {src}")
        return None
    
    # Compile with hardening flags
    cmd = [
        "x86_64-w64-mingw32-gcc",
        "-O2", "-static", "-s",
        "-Wl,--dynamicbase",      # ASLR
        "-Wl,--nxcompat",         # DEP
        "-fstack-protector-strong", # GS
        "-fno-ident",             # Remove compiler info
        "-DNDEBUG",               # Release mode
        src, "-o", dst
    ]
    
    try:
        subprocess.check_call(cmd, stderr=subprocess.PIPE)
        print(f"[+] Built level_{level_num:02d}.exe")
        
        # Calculate hash
        hash_val = calculate_hash(dst)
        
        # Get file size
        size = os.path.getsize(dst)
        
        return {
            "arch": "x64",
            "technique": f"level_{level_num:02d}",
            "hash": hash_val,
            "size": size,
            "compiler": "x86_64-w64-mingw32-gcc",
            "flags": ["ASLR", "DEP", "GS", "static"]
        }
        
    except subprocess.CalledProcessError as e:
        print(f"[!] Build failed for level_{level_num:02d}: {e}")
        return None

def build_all_levels() -> bool:
    """Build all levels 1-9"""
    print("[LAB-9] Building all levels with hardening...")
    
    # Create bin directory
    bin_dir = os.path.join(PROJECT_ROOT, "bin")
    os.makedirs(bin_dir, exist_ok=True)
    
    success_count = 0
    
    for level in range(1, 10):
        result = build_level(level)
        if result:
            MANIFEST["levels"][level] = result
            success_count += 1
        else:
            print(f"[!] Failed to build level {level}")
    
    # Save manifest
    manifest_path = os.path.join(bin_dir, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(MANIFEST, f, indent=2)
    
    # Generate checksums
    checksums = []
    for level in range(1, 10):
        exe_path = os.path.join(bin_dir, f"level_{level:02d}.exe")
        if os.path.exists(exe_path):
            hash_val = calculate_hash(exe_path)
            checksums.append(f"{hash_val}  level_{level:02d}.exe")
    
    checksums_path = os.path.join(bin_dir, "sha256sums.txt")
    with open(checksums_path, "w") as f:
        f.write("\n".join(checksums))
    
    print(f"[+] Built {success_count}/9 levels successfully")
    print(f"[+] Manifest saved to {manifest_path}")
    print(f"[+] Checksums saved to {checksums_path}")
    
    return success_count == 9

def verify_builds() -> bool:
    """Verify all builds are deterministic"""
    print("[LAB-9] Verifying deterministic builds...")
    
    for level in range(1, 10):
        exe_path = os.path.join(PROJECT_ROOT, f"bin/level_{level:02d}.exe")
        if not os.path.exists(exe_path):
            print(f"[!] Missing: {exe_path}")
            return False
        
        # Check if hash matches manifest
        current_hash = calculate_hash(exe_path)
        expected_hash = MANIFEST["levels"][level]["hash"]
        
        if current_hash != expected_hash:
            print(f"[!] Hash mismatch for level_{level:02d}")
            return False
    
    print("[+] All builds verified successfully")
    return True

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--level":
            level_num = int(sys.argv[2])
            result = build_level(level_num)
            if result:
                print(f"[+] Level {level_num} built successfully")
            else:
                print(f"[!] Failed to build level {level_num}")
        elif sys.argv[1] == "--verify":
            if verify_builds():
                print("[+] Verification passed")
            else:
                print("[!] Verification failed")
                sys.exit(1)
        else:
            print("Usage: build.py [--level N] [--verify]")
    else:
        if build_all_levels():
            print("[+] All levels built successfully")
        else:
            print("[!] Some levels failed to build")
            sys.exit(1)

if __name__ == "__main__":
    main() 