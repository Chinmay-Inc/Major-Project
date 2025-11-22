"""
Enhanced launcher script for AI Investment Advisor
Handles common issues and provides better error messages
"""
import subprocess
import sys
import os
import importlib.util

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def check_and_install_dependencies():
    """Check and install required dependencies"""
    required_packages = [
        "streamlit",
        "pandas", 
        "numpy",
        "scikit-learn",
        "tensorflow",
        "yfinance",
        "matplotlib",
        "plotly",
        "seaborn",
        "reportlab",
        "streamlit-authenticator",
        "bcrypt"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == "tensorflow":
                import tensorflow as tf
            elif package == "streamlit-authenticator":
                import streamlit_authenticator
            else:
                __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        
        for package in missing_packages:
            print(f"Installing {package}...")
            if install_package(package):
                print(f"✅ {package} installed successfully")
            else:
                print(f"❌ Failed to install {package}")
                return False
    
    return True

def check_app_files():
    """Check if all required app files exist"""
    required_files = [
        "app.py",
        "financial_analyzer.py", 
        "visualizations.py",
        "auth_manager.py",
        "pdf_generator.py",
        "config.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files found")
    return True

def test_imports():
    """Test if the app can be imported"""
    try:
        # Test individual modules
        from financial_analyzer import FinancialAnalyzer
        from visualizations import InvestmentVisualizer
        from auth_manager import AuthManager
        from pdf_generator import PDFGenerator
        
        print("✅ All modules imported successfully")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def launch_app():
    """Launch the Streamlit app"""
    try:
        print("🚀 Launching AI Investment Advisor...")
        print("=" * 50)
        print("The app will open in your default browser.")
        print("If it doesn't open automatically, go to: http://localhost:8501")
        print("=" * 50)
        
        # Launch Streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py", "--server.headless", "false"])
        
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user.")
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure you're in the correct directory")
        print("2. Try running: pip install --upgrade streamlit")
        print("3. Check if port 8501 is available")

def main():
    """Main launcher function"""
    print("🤖 AI Investment Advisor - Enhanced Launcher")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Check if we're in the right directory
    if not check_app_files():
        print("\n💡 Make sure you're running this script from the project directory")
        return False
    
    # Check and install dependencies
    if not check_and_install_dependencies():
        print("\n❌ Failed to install dependencies. Please install manually:")
        print("pip install -r requirements.txt")
        return False
    
    # Test imports
    if not test_imports():
        print("\n❌ Import test failed. Please check the error above.")
        return False
    
    print("\n🎉 All checks passed! Launching application...")
    
    # Launch the app
    launch_app()
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ Setup failed. Please fix the issues above and try again.")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
