#!/usr/bin/env python3
"""
Dependency Checker (Read-Only)
Checks if all required packages are installed without installing anything.
"""

import subprocess
import sys
import importlib
import pkg_resources

# Required packages with their versions
REQUIRED_PACKAGES = {
    'flask': '2.3.3',
    'flask-cors': '4.0.0',
    'PyJWT': '2.8.0',
    'requests': '2.31.0'
}

def check_package(package_name, required_version=None):
    """Check if a package is installed and return its version"""
    try:
        # Try to import the package
        module = importlib.import_module(package_name)
        
        # Get the installed version
        if hasattr(module, '__version__'):
            installed_version = module.__version__
        else:
            # Try to get version from pkg_resources
            try:
                installed_version = pkg_resources.get_distribution(package_name).version
            except:
                installed_version = "unknown"
        
        print(f"✅ {package_name} - Installed (version: {installed_version})")
        return True, installed_version
        
    except ImportError:
        print(f"❌ {package_name} - Not installed")
        return False, None
    except Exception as e:
        print(f"⚠️ {package_name} - Error checking: {e}")
        return False, None

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("⚠️ Warning: Python 3.7+ is recommended")
        return False
    else:
        print("✅ Python version is compatible")
        return True

def check_pip():
    """Check if pip is available"""
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"📦 pip is available: {result.stdout.strip()}")
            return True
        else:
            print("❌ pip is not available")
            return False
    except Exception as e:
        print(f"❌ Error checking pip: {e}")
        return False

def main():
    """Main function to check dependencies"""
    print("🔍 Dependency Checker (Read-Only)")
    print("=" * 50)
    
    # Check Python version
    print("\n1. Checking Python version...")
    check_python_version()
    
    # Check pip
    print("\n2. Checking pip...")
    check_pip()
    
    # Check each required package
    print("\n3. Checking required packages...")
    print("-" * 50)
    
    missing_packages = []
    installed_packages = []
    
    for package, version in REQUIRED_PACKAGES.items():
        is_installed, installed_version = check_package(package, version)
        
        if is_installed:
            installed_packages.append(package)
        else:
            missing_packages.append((package, version))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY:")
    print(f"✅ Installed packages: {len(installed_packages)}")
    print(f"❌ Missing packages: {len(missing_packages)}")
    
    if installed_packages:
        print(f"✅ Installed: {', '.join(installed_packages)}")
    
    if missing_packages:
        print(f"❌ Missing: {', '.join([pkg for pkg, _ in missing_packages])}")
        print("\n💡 To install missing packages, run:")
        print("   python check_requirements.py")
        print("   or")
        print("   pip install -r requirements.txt")
    
    if not missing_packages:
        print("\n✅ All required packages are installed!")
        print("🚀 You can now run the server with: python server.py")
    else:
        print("\n⚠️ Some packages are missing. Install them to run the application.")

if __name__ == '__main__':
    main() 