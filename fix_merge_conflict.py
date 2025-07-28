#!/usr/bin/env python3
"""
Automatic Git Merge Conflict Resolver for StockTrendAI
Specifically handles data/notifications.json conflicts
"""

import subprocess
import sys
import os
from datetime import datetime

def run_command(command, capture_output=True):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=capture_output, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_git_status():
    """Check current git status"""
    success, stdout, stderr = run_command("git status --porcelain")
    if success:
        return stdout.strip().split('\n') if stdout.strip() else []
    return []

def fix_notifications_conflict():
    """Automatically fix notifications.json merge conflict"""
    print("🔧 AUTOMATIC MERGE CONFLICT RESOLVER")
    print("=" * 40)
    print()
    
    # Check if we're in a git repository
    if not os.path.exists('.git'):
        print("❌ Not in a git repository")
        return False
    
    # Check git status
    print("📋 Checking git status...")
    status_lines = check_git_status()
    
    notifications_modified = False
    for line in status_lines:
        if 'data/notifications.json' in line:
            notifications_modified = True
            print(f"📁 Found: {line}")
    
    if not notifications_modified:
        print("✅ No notifications.json conflicts detected")
        print("🎯 You can now safely run: git pull origin main")
        return True
    
    print()
    print("🔧 RESOLVING NOTIFICATIONS.JSON CONFLICT:")
    print("-" * 42)
    
    # Option 1: Try to commit the changes
    print("📝 Attempting to commit current changes...")
    
    success, stdout, stderr = run_command("git add data/notifications.json")
    if not success:
        print(f"❌ Failed to add file: {stderr}")
        return False
    
    commit_message = f"🔔 Update notifications.json - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    success, stdout, stderr = run_command(f'git commit -m "{commit_message}"')
    
    if success:
        print(f"✅ Successfully committed changes: {commit_message}")
        
        # Now try to pull
        print("📥 Attempting to pull from origin...")
        success, stdout, stderr = run_command("git pull origin main")
        
        if success:
            print("✅ Successfully pulled from origin/main")
            print("🎉 Merge conflict resolved!")
            return True
        else:
            print(f"⚠️ Pull failed: {stderr}")
            print("💡 You may need to resolve conflicts manually")
            return False
    else:
        print(f"⚠️ Commit failed: {stderr}")
        print()
        print("🔄 TRYING ALTERNATIVE APPROACH...")
        
        # Option 2: Stash changes and pull
        print("📦 Stashing changes...")
        success, stdout, stderr = run_command("git stash push -m 'Auto-stash notifications before merge'")
        
        if success:
            print("✅ Changes stashed successfully")
            
            # Pull from origin
            success, stdout, stderr = run_command("git pull origin main")
            
            if success:
                print("✅ Successfully pulled from origin/main")
                
                # Try to pop stash
                print("📦 Restoring stashed changes...")
                success, stdout, stderr = run_command("git stash pop")
                
                if success:
                    print("✅ Stashed changes restored")
                    print("🎉 Merge conflict resolved!")
                    return True
                else:
                    print(f"⚠️ Stash pop failed: {stderr}")
                    print("💡 Your changes are still in stash. Use: git stash list")
                    return False
            else:
                print(f"❌ Pull failed: {stderr}")
                return False
        else:
            print(f"❌ Stash failed: {stderr}")
            return False

def main():
    """Main function"""
    print("🚀 StockTrendAI - Git Merge Conflict Auto-Resolver")
    print("=" * 50)
    print()
    
    success = fix_notifications_conflict()
    
    print()
    if success:
        print("🎯 CONFLICT RESOLUTION SUCCESSFUL!")
        print("✅ Your repository is now up-to-date")
        print("🚀 You can continue working normally")
    else:
        print("⚠️ AUTOMATIC RESOLUTION FAILED")
        print()
        print("📋 MANUAL STEPS TO RESOLVE:")
        print("1. git status")
        print("2. git add data/notifications.json")
        print("3. git commit -m 'Update notifications'")
        print("4. git pull origin main")
        print()
        print("OR use stash approach:")
        print("1. git stash")
        print("2. git pull origin main")
        print("3. git stash pop")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)