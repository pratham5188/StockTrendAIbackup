#!/usr/bin/env python3
"""
Comprehensive Dependency Installation Script for StockTrendAI
Ensures all required modules are properly installed
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False

def check_and_install_dependencies():
    """Check and install all required dependencies"""
    print("🔍 COMPREHENSIVE DEPENDENCY CHECK AND INSTALLATION")
    print("=" * 55)
    print()
    
    # Core dependencies from requirements.txt
    dependencies = [
        "streamlit>=1.47.0",
        "pandas>=2.3.1", 
        "numpy<2.0",
        "plotly>=6.2.0",
        "scikit-learn>=1.7.0",
        "yfinance>=0.2.65",
        "xgboost>=3.0.2",
        "textblob>=0.19.0",
        "prophet>=1.1.7",
        "lightgbm>=4.6.0",
        "matplotlib>=3.10.0",
        "cmdstanpy>=1.0.4",
        "holidays>=0.25",
        "importlib_resources>=6.5.2",
        "scipy>=1.16.0",
        "schedule>=1.2.0",
        "requests>=2.31.0",
        "pytz>=2024.1"
    ]
    
    failed_installs = []
    successful_installs = []
    
    for dep in dependencies:
        print(f"📦 Installing {dep}...")
        if install_package(dep):
            successful_installs.append(dep)
        else:
            failed_installs.append(dep)
    
    print()
    print("📊 INSTALLATION SUMMARY:")
    print("-" * 26)
    print(f"✅ Successful: {len(successful_installs)}")
    print(f"❌ Failed: {len(failed_installs)}")
    
    if failed_installs:
        print()
        print("❌ FAILED INSTALLATIONS:")
        for dep in failed_installs:
            print(f"  - {dep}")
        print()
        print("🔧 MANUAL INSTALLATION COMMANDS:")
        for dep in failed_installs:
            print(f"pip install {dep}")
    else:
        print()
        print("🎉 ALL DEPENDENCIES INSTALLED SUCCESSFULLY!")
    
    # Test imports
    print()
    print("🧪 TESTING IMPORTS:")
    print("-" * 17)
    
    test_imports = [
        ("streamlit", "streamlit"),
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("plotly", "plotly"),
        ("yfinance", "yfinance"),
        ("xgboost", "xgboost"),
        ("prophet", "prophet"),
        ("schedule", "schedule"),
        ("requests", "requests"),
        ("pytz", "pytz")
    ]
    
    import_failures = []
    
    for import_name, package_name in test_imports:
        try:
            __import__(import_name)
            print(f"✅ {import_name}: OK")
        except ImportError as e:
            print(f"❌ {import_name}: FAILED - {e}")
            import_failures.append((import_name, package_name))
    
    if import_failures:
        print()
        print("⚠️ IMPORT FAILURES DETECTED:")
        for import_name, package_name in import_failures:
            print(f"  {import_name} ({package_name})")
        return False
    else:
        print()
        print("✅ ALL IMPORTS SUCCESSFUL!")
        return True

if __name__ == "__main__":
    success = check_and_install_dependencies()
    
    if success:
        print()
        print("🎯 READY TO RUN STOCKTRENDAI!")
        print("Run with: streamlit run app.py")
    else:
        print()
        print("❌ PLEASE RESOLVE DEPENDENCY ISSUES BEFORE RUNNING")
        sys.exit(1)