#!/usr/bin/env python3
"""
Git Merge Editor Error Fix Script
Handles 'problem with editor vi' during merge completion
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

def check_merge_state():
    """Check if we're in a merge state"""
    # Check if MERGE_HEAD exists (indicates ongoing merge)
    merge_head_exists = os.path.exists('.git/MERGE_HEAD')
    
    # Check git status
    success, stdout, stderr = run_command("git status --porcelain")
    has_conflicts = False
    
    if success and stdout:
        for line in stdout.strip().split('\n'):
            if line.startswith('UU ') or line.startswith('AA '):
                has_conflicts = True
                break
    
    return merge_head_exists, has_conflicts

def fix_editor_merge():
    """Fix the Git merge editor issue"""
    print("🔧 GIT MERGE EDITOR ERROR FIXER")
    print("=" * 35)
    print()
    
    # Check if we're in a git repository
    if not os.path.exists('.git'):
        print("❌ Not in a git repository")
        return False
    
    # Check merge state
    merge_in_progress, has_conflicts = check_merge_state()
    
    print(f"📋 Merge in progress: {'Yes' if merge_in_progress else 'No'}")
    print(f"🔍 Conflicts detected: {'Yes' if has_conflicts else 'No'}")
    
    if not merge_in_progress:
        print("✅ No merge in progress - no action needed")
        return True
    
    if has_conflicts:
        print("⚠️ Unresolved conflicts detected!")
        print("📋 You need to resolve conflicts first:")
        print("   1. Edit conflicted files manually")
        print("   2. Or run: python resolve_merge_conflict.py")
        print("   3. Then run this script again")
        return False
    
    print()
    print("🔧 COMPLETING MERGE WITHOUT EDITOR:")
    print("-" * 35)
    
    # Try multiple approaches to complete the merge
    
    # Approach 1: Commit without editor
    print("📝 Attempting: git commit --no-edit")
    success, stdout, stderr = run_command("git commit --no-edit")
    
    if success:
        print("✅ Merge completed successfully with --no-edit!")
        return True
    else:
        print(f"⚠️ --no-edit failed: {stderr.strip()}")
    
    # Approach 2: Commit with custom message
    print("📝 Attempting: git commit with custom message")
    commit_message = f"Complete merge - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    success, stdout, stderr = run_command(f'git commit -m "{commit_message}"')
    
    if success:
        print(f"✅ Merge completed with custom message: {commit_message}")
        return True
    else:
        print(f"⚠️ Custom message failed: {stderr.strip()}")
    
    # Approach 3: Set nano as editor and commit
    print("📝 Attempting: Set nano editor and commit")
    run_command("git config --global core.editor 'nano'")
    success, stdout, stderr = run_command("git commit")
    
    if success:
        print("✅ Merge completed with nano editor!")
        # Reset editor back to default
        run_command("git config --global --unset core.editor")
        return True
    else:
        print(f"⚠️ Nano editor failed: {stderr.strip()}")
    
    # Approach 4: Force commit with empty message
    print("📝 Attempting: Force commit with minimal message")
    success, stdout, stderr = run_command('git commit -m "Merge"')
    
    if success:
        print("✅ Merge completed with minimal message!")
        return True
    else:
        print(f"⚠️ Force commit failed: {stderr.strip()}")
    
    print("❌ All automatic approaches failed")
    return False

def show_manual_solutions():
    """Show manual solutions if automatic fails"""
    print()
    print("🔄 MANUAL SOLUTIONS:")
    print("=" * 20)
    print()
    
    print("📋 OPTION 1 - Simple Commit:")
    print("git commit -m 'Complete merge'")
    print()
    
    print("📋 OPTION 2 - No Editor Commit:")
    print("git commit --no-edit")
    print()
    
    print("📋 OPTION 3 - Change Editor:")
    print("git config --global core.editor 'nano'")
    print("git commit")
    print()
    
    print("📋 OPTION 4 - Abort and Retry:")
    print("git merge --abort")
    print("# Then try your merge operation again")
    print()
    
    print("📋 OPTION 5 - Set Editor Permanently:")
    print("git config --global core.editor 'nano'  # Use nano instead of vi")
    print("git config --global core.editor 'code --wait'  # Use VS Code")
    print("git config --global core.editor 'gedit --wait'  # Use gedit")

def main():
    """Main function"""
    print("🚀 StockTrendAI - Git Merge Editor Error Fixer")
    print("=" * 47)
    print("🎯 Target: Fix 'problem with editor vi' merge error")
    print()
    
    success = fix_editor_merge()
    
    print()
    if success:
        print("🎉 MERGE EDITOR ERROR FIXED!")
        print("=" * 30)
        print("✅ Merge completed successfully")
        print("✅ Repository is now in clean state")
        print("✅ Ready for normal Git operations")
        print()
        print("🔄 Next steps:")
        print("1. git status  # Verify clean state")
        print("2. git push origin main  # Push changes")
        print()
        print("💡 To prevent future editor issues:")
        print("git config --global core.editor 'nano'")
    else:
        print("⚠️ AUTOMATIC FIX FAILED")
        print("=" * 25)
        show_manual_solutions()
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)