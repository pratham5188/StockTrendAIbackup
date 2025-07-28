#!/usr/bin/env python3
"""
Advanced Git Merge Conflict Resolver for data/notifications.json
Handles the specific CONFLICT(content) error in notifications.json
"""

import subprocess
import sys
import os
import json
from datetime import datetime

def run_command(command, capture_output=True):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=capture_output, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_merge_conflict():
    """Check if we're in a merge conflict state"""
    # Check if MERGE_HEAD exists (indicates ongoing merge)
    merge_head_exists = os.path.exists('.git/MERGE_HEAD')
    
    # Check git status for conflict markers
    success, stdout, stderr = run_command("git status --porcelain")
    conflict_files = []
    
    if success and stdout:
        for line in stdout.strip().split('\n'):
            if line.startswith('UU ') or line.startswith('AA '):  # Both modified/added
                conflict_files.append(line[3:])
    
    return merge_head_exists, conflict_files

def resolve_notifications_conflict():
    """Resolve the notifications.json merge conflict"""
    print("🔧 MERGE CONFLICT RESOLVER - ADVANCED")
    print("=" * 42)
    print()
    
    # Check if we're in a git repository
    if not os.path.exists('.git'):
        print("❌ Not in a git repository")
        return False
    
    # Check merge conflict state
    merge_in_progress, conflict_files = check_merge_conflict()
    
    print(f"📋 Merge in progress: {'Yes' if merge_in_progress else 'No'}")
    print(f"📁 Conflict files: {conflict_files}")
    
    # Handle the specific case of notifications.json conflict
    notifications_file = "data/notifications.json"
    
    if os.path.exists(notifications_file):
        print(f"📄 Found {notifications_file}")
        
        # Read the file to check for conflict markers
        try:
            with open(notifications_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for Git conflict markers
            has_conflict_markers = any(marker in content for marker in ['<<<<<<<', '=======', '>>>>>>>'])
            
            if has_conflict_markers:
                print("⚠️ Conflict markers detected in notifications.json")
                print("🔧 Resolving conflict automatically...")
                
                # Strategy: Keep the local version and create a clean notifications file
                clean_notifications = {
                    "notifications": [],
                    "last_saved": datetime.now().isoformat()
                }
                
                # Try to extract valid notifications from both sides
                lines = content.split('\n')
                local_section = []
                remote_section = []
                current_section = None
                
                for line in lines:
                    if line.strip().startswith('<<<<<<<'):
                        current_section = 'local'
                        continue
                    elif line.strip().startswith('======='):
                        current_section = 'remote'
                        continue
                    elif line.strip().startswith('>>>>>>>'):
                        current_section = None
                        continue
                    
                    if current_section == 'local':
                        local_section.append(line)
                    elif current_section == 'remote':
                        remote_section.append(line)
                
                # Try to parse local section first
                try:
                    local_content = '\n'.join(local_section)
                    if local_content.strip():
                        local_data = json.loads(local_content)
                        if 'notifications' in local_data:
                            clean_notifications = local_data
                            print("✅ Using local notifications data")
                except json.JSONDecodeError:
                    print("⚠️ Local section invalid, trying remote...")
                    
                    # Try remote section
                    try:
                        remote_content = '\n'.join(remote_section)
                        if remote_content.strip():
                            remote_data = json.loads(remote_content)
                            if 'notifications' in remote_data:
                                clean_notifications = remote_data
                                print("✅ Using remote notifications data")
                    except json.JSONDecodeError:
                        print("⚠️ Both sections invalid, creating fresh notifications")
                
                # Write the resolved content
                with open(notifications_file, 'w', encoding='utf-8') as f:
                    json.dump(clean_notifications, f, indent=2, ensure_ascii=False)
                
                print(f"✅ Resolved conflict in {notifications_file}")
                
            else:
                print("✅ No conflict markers found in notifications.json")
        
        except Exception as e:
            print(f"⚠️ Error reading notifications.json: {e}")
            # Create a fresh notifications file
            clean_notifications = {
                "notifications": [],
                "last_saved": datetime.now().isoformat()
            }
            
            with open(notifications_file, 'w', encoding='utf-8') as f:
                json.dump(clean_notifications, f, indent=2, ensure_ascii=False)
            
            print("✅ Created fresh notifications.json")
    
    # Add the resolved file
    print("📝 Adding resolved file to git...")
    success, stdout, stderr = run_command(f"git add {notifications_file}")
    
    if not success:
        print(f"❌ Failed to add {notifications_file}: {stderr}")
        return False
    
    print("✅ File added successfully")
    
    # Complete the merge
    if merge_in_progress:
        print("🔄 Completing the merge...")
        success, stdout, stderr = run_command("git commit --no-edit")
        
        if success:
            print("✅ Merge completed successfully!")
            return True
        else:
            # Try with a custom message
            commit_msg = f"Resolve merge conflict in {notifications_file}"
            success, stdout, stderr = run_command(f'git commit -m "{commit_msg}"')
            
            if success:
                print("✅ Merge completed with custom message!")
                return True
            else:
                print(f"❌ Failed to complete merge: {stderr}")
                return False
    else:
        print("✅ No merge in progress, conflict resolved")
        return True

def show_alternative_solutions():
    """Show alternative manual solutions"""
    print()
    print("🔄 ALTERNATIVE MANUAL SOLUTIONS:")
    print("=" * 35)
    print()
    
    print("📋 OPTION 1 - Use Local Version:")
    print("git checkout --ours data/notifications.json")
    print("git add data/notifications.json")
    print("git commit")
    print()
    
    print("📋 OPTION 2 - Use Remote Version:")
    print("git checkout --theirs data/notifications.json")
    print("git add data/notifications.json") 
    print("git commit")
    print()
    
    print("📋 OPTION 3 - Abort Merge:")
    print("git merge --abort")
    print("# Then try a different approach")
    print()
    
    print("📋 OPTION 4 - Manual Edit:")
    print("1. Open data/notifications.json in editor")
    print("2. Remove conflict markers: <<<<<<<, =======, >>>>>>>")
    print("3. Keep the content you want")
    print("4. Save the file")
    print("5. git add data/notifications.json")
    print("6. git commit")

def main():
    """Main function"""
    print("🚀 StockTrendAI - Advanced Merge Conflict Resolver")
    print("=" * 52)
    print("🎯 Target: CONFLICT(content) in data/notifications.json")
    print()
    
    success = resolve_notifications_conflict()
    
    print()
    if success:
        print("🎉 MERGE CONFLICT RESOLUTION SUCCESSFUL!")
        print("=" * 40)
        print("✅ notifications.json conflict resolved")
        print("✅ Changes committed to repository")
        print("✅ Ready to continue normal operations")
        print()
        print("🔄 Next steps:")
        print("1. git status  # Verify clean state")
        print("2. git push origin main  # Push changes")
    else:
        print("⚠️ AUTOMATIC RESOLUTION FAILED")
        print("=" * 32)
        show_alternative_solutions()
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)