#!/usr/bin/env python3
# LAB-9 v2.1 - CLI Tool
# Author: Lethe

import click, subprocess, os, sys, json
from typing import Dict, Any

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

@click.group()
@click.version_option(version="2.1")
def cli():
    """LAB-9 Reverse Warfare Trainer CLI"""
    pass

@cli.command()
@click.option('--level', type=int, help='Build specific level')
@click.option('--all', is_flag=True, help='Build all levels')
@click.option('--verify', is_flag=True, help='Verify builds after compilation')
def build(level, all, verify):
    """Build levels"""
    build_script = os.path.join(PROJECT_ROOT, 'tools', 'build.py')
    
    if all:
        print("[LAB-9] Building all levels...")
        result = subprocess.run(['python', build_script], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        if result.returncode != 0:
            sys.exit(1)
    elif level:
        print(f"[LAB-9] Building level {level}...")
        result = subprocess.run(['python', build_script, '--level', str(level)], 
                              capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        if result.returncode != 0:
            sys.exit(1)
    else:
        print("[LAB-9] Building all levels...")
        result = subprocess.run(['python', build_script], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        if result.returncode != 0:
            sys.exit(1)
    
    if verify:
        print("[LAB-9] Verifying builds...")
        result = subprocess.run(['python', build_script, '--verify'], 
                              capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)

@cli.command()
@click.option('--level', type=int, help='Test specific level')
@click.option('--all', is_flag=True, help='Test all levels')
@click.option('--scenario', type=click.Choice(['no_debugger', 'partial_patch']), 
              default='no_debugger', help='Test scenario')
def test(level, all, scenario):
    """Run tests"""
    if scenario == 'no_debugger':
        test_script = os.path.join(PROJECT_ROOT, 'tests', 'test_no_dbg.py')
    elif scenario == 'partial_patch':
        test_script = os.path.join(PROJECT_ROOT, 'tests', 'test_partial_patch.py')
    
    if all:
        print(f"[LAB-9] Running {scenario} tests for all levels...")
        result = subprocess.run(['python', test_script], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        if result.returncode != 0:
            sys.exit(1)
    elif level:
        print(f"[LAB-9] Running {scenario} test for level {level}...")
        result = subprocess.run(['python', test_script, str(level)], 
                              capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        if result.returncode != 0:
            sys.exit(1)
    else:
        print(f"[LAB-9] Running {scenario} tests for all levels...")
        result = subprocess.run(['python', test_script], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        if result.returncode != 0:
            sys.exit(1)

@cli.command()
@click.option('--level', type=int, required=True, help='Level number')
@click.option('--format', type=click.Choice(['md', 'txt']), default='md', help='Output format')
def walkthrough(level, format):
    """Generate walkthrough for level"""
    walkthrough_path = os.path.join(PROJECT_ROOT, 'solutions', 'walkthroughs', f'level_{level:02d}_walkthrough.md')
    
    if not os.path.exists(walkthrough_path):
        print(f"[!] Walkthrough not found: {walkthrough_path}")
        sys.exit(1)
    
    with open(walkthrough_path, 'r') as f:
        content = f.read()
    
    if format == 'txt':
        # Convert markdown to plain text
        import re
        content = re.sub(r'#+ ', '', content)
        content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)
        content = re.sub(r'`(.*?)`', r'\1', content)
    
    print(content)

@cli.command()
@click.option('--level', type=int, required=True, help='Level number')
@click.option('--addr', type=str, required=True, help='Address to patch')
@click.option('--bytes', type=str, required=True, help='New bytes (hex)')
def patch(level, addr, bytes):
    """Generate patch for level"""
    patch_path = os.path.join(PROJECT_ROOT, 'tools', 'x64dbg_patches', f'level_{level:02d}.1337')
    
    if not os.path.exists(patch_path):
        print(f"[!] Patch file not found: {patch_path}")
        sys.exit(1)
    
    with open(patch_path, 'r') as f:
        content = f.read()
    
    # Add new patch
    new_patch = f"\n# Manual patch\n{addr}: {bytes}\n"
    content += new_patch
    
    print(f"[+] Patch added to {patch_path}")
    print(f"[+] Address: {addr}")
    print(f"[+] Bytes: {bytes}")

@cli.command()
def status():
    """Show project status"""
    print("[LAB-9] Project Status")
    print("=" * 50)
    
    # Check levels
    levels_built = 0
    for i in range(1, 10):
        exe_path = os.path.join(PROJECT_ROOT, 'bin', f'level_{i:02d}.exe')
        if os.path.exists(exe_path):
            levels_built += 1
    
    print(f"Levels built: {levels_built}/9")
    
    # Check tests
    tests_passed = 0
    results_path = os.path.join(PROJECT_ROOT, 'tests', 'results_no_debugger.json')
    if os.path.exists(results_path):
        with open(results_path, 'r') as f:
            results = json.load(f)
            tests_passed = sum(1 for r in results if r['status'] == 'PASS')
    
    print(f"Tests passed: {tests_passed}/9")
    
    # Check manifest
    manifest_path = os.path.join(PROJECT_ROOT, 'bin', 'manifest.json')
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
            print(f"Architecture: {manifest.get('architecture', 'Unknown')}")
            print(f"Version: {manifest.get('version', 'Unknown')}")
    
    print("=" * 50)

@cli.command()
def clean():
    """Clean build artifacts"""
    import shutil
    
    print("[LAB-9] Cleaning build artifacts...")
    
    # Remove bin directory
    bin_path = os.path.join(PROJECT_ROOT, 'bin')
    if os.path.exists(bin_path):
        shutil.rmtree(bin_path)
        print("[+] Removed bin/ directory")
    
    # Remove test results
    for result_file in ["results_no_debugger.json", "results_partial_patch.json"]:
        result_path = os.path.join(PROJECT_ROOT, 'tests', result_file)
        if os.path.exists(result_path):
            os.remove(result_path)
            print(f"[+] Removed {result_file}")
    
    print("[+] Clean completed")

if __name__ == '__main__':
    cli() 