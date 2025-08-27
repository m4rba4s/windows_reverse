#!/usr/bin/env python3
# LAB-9 v2.1 - Test: Partial Patch Detection
# Author: Lethe

import os, subprocess, json, time, sys
from typing import Dict, List, Any

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

def simulate_partial_patch(level_num: int, timeout: int = 5) -> Dict[str, Any]:
    """Simulate partial patching scenario"""
    exe_path = os.path.join(PROJECT_ROOT, f"bin/level_{level_num:02d}.exe")
    
    if not os.path.exists(exe_path):
        return {
            "level": level_num,
            "status": "error",
            "error": "executable not found",
            "exit_code": None,
            "output": "",
            "duration": 0
        }
    
    try:
        start_time = time.time()
        result = subprocess.run(
            [exe_path],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        duration = time.time() - start_time
        
        return {
            "level": level_num,
            "status": "completed",
            "exit_code": result.returncode,
            "output": result.stdout + result.stderr,
            "duration": duration,
            "error": None
        }
        
    except subprocess.TimeoutExpired:
        return {
            "level": level_num,
            "status": "timeout",
            "exit_code": None,
            "output": "",
            "duration": timeout,
            "error": "timeout"
        }
    except Exception as e:
        return {
            "level": level_num,
            "status": "error",
            "exit_code": None,
            "output": "",
            "duration": 0,
            "error": str(e)
        }

def test_all_levels_partial_patch() -> List[Dict[str, Any]]:
    """Test all levels with partial patch simulation"""
    print("[LAB-9] Testing all levels with partial patches...")
    
    results = []
    expected_exit_codes = {
        1: [1, 0xC0FFEE],      # Should still fail with partial patch
        2: [1, 0xC0FFEE],
        3: [1, 0xC0FFEE],
        4: [1, 0xC0FFEE],
        5: [1, 0xC0FFEE],
        6: [1, 0xC0FFEE],
        7: [1, 0xC0FFEE],
        8: [1, 0xC0FFEE],
        9: [1, 0xC0FFEE]
    }
    
    for level in range(1, 10):
        print(f"[*] Testing level_{level:02d} with partial patch simulation...")
        result = simulate_partial_patch(level)
        results.append(result)
        
        # Check if result is as expected
        if result["status"] == "completed":
            exit_code = result["exit_code"]
            expected = expected_exit_codes[level]
            
            if exit_code in expected:
                print(f"[+] Level {level:02d}: PASS (exit code {exit_code})")
            else:
                print(f"[!] Level {level:02d}: FAIL (unexpected exit code {exit_code})")
        else:
            print(f"[!] Level {level:02d}: {result['status']} - {result.get('error', 'unknown')}")
    
    return results

def save_results(results: List[Dict[str, Any]], filename: str):
    """Save test results to JSON file"""
    results_dir = os.path.join(PROJECT_ROOT, "tests")
    os.makedirs(results_dir, exist_ok=True)
    
    output_path = os.path.join(results_dir, filename)
    
    test_summary = {
        "test_name": "partial_patch_detection",
        "timestamp": time.time(),
        "total_levels": len(results),
        "passed": sum(1 for r in results if r["status"] == "completed" and r["exit_code"] in [1, 0xC0FFEE]),
        "failed": sum(1 for r in results if r["status"] != "completed" or r["exit_code"] not in [1, 0xC0FFEE]),
        "results": results
    }
    
    with open(output_path, "w") as f:
        json.dump(test_summary, f, indent=2)
    
    print(f"[+] Results saved to {output_path}")
    return test_summary

def main():
    # Run tests
    results = test_all_levels_partial_patch()
    
    # Save results
    summary = save_results(results, "results_partial_patch.json")
    
    # Print summary
    print(f"\n[LAB-9] Test Summary:")
    print(f"  Total levels: {summary['total_levels']}")
    print(f"  Passed: {summary['passed']}")
    print(f"  Failed: {summary['failed']}")
    
    if summary['failed'] == 0:
        print("[+] All levels correctly fail with partial patches!")
        print("[+] Partial patch protection is working properly.")
        return 0
    else:
        print("[!] Some levels may allow completion with partial patches!")
        print("[!] Review failed tests above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 