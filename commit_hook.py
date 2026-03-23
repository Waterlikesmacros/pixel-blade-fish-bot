#!/usr/bin/env python3
"""
Simple Git commit hook for Windows that generates automatic commit messages
"""
import subprocess
import sys
import os

def get_changed_files():
    """Get list of changed files"""
    try:
        result = subprocess.run(['git', 'diff', '--cached', '--name-only'], 
                          capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            files = result.stdout.strip().split('\n')
            return [f for f in files if f.strip()]
    except:
        return []

def generate_commit_message():
    """Generate commit message based on changes"""
    files = get_changed_files()
    
    if not files:
        return "Fishing Macro update: minor changes"
    
    # Count file types
    added = [f for f in files if os.path.exists(f)]
    modified = [f for f in files if not f.startswith('.git')]
    
    if added:
        return f"Fishing Macro update: added {len(added)} files"
    elif modified:
        return f"Fishing Macro update: modified {len(modified)} files"
    else:
        return "Fishing Macro update"

def main():
    """Main hook function"""
    # Get commit message from argument or generate one
    if len(sys.argv) > 1:
        message = ' '.join(sys.argv[1:])
    else:
        message = generate_commit_message()
    
    # Write message to file for Git to use
    with open('.git/COMMIT_EDITMSG', 'w') as f:
        f.write(message)

if __name__ == "__main__":
    main()
