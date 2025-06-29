#!/usr/bin/env python3
"""
Setup script for CS50 AI Search Project
Installs required dependencies and provides usage instructions.
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def check_pyside6():
    """Check if PySide6 is working"""
    try:
        import PySide6
        print("✅ PySide6 is available")
        return True
    except ImportError:
        print("❌ PySide6 not found. Please install it manually:")
        print("   pip install PySide6")
        return False

def main():
    """Main setup function"""
    print("=" * 60)
    print("CS50 AI SEARCH PROJECT SETUP")
    print("=" * 60)
    
    # Install requirements
    if not install_requirements():
        print("\nSetup failed. Please install requirements manually:")
        print("pip install -r requirements.txt")
        return
    
    # Check PySide6
    if not check_pyside6():
        print("\nPySide6 is required for the interactive game.")
        print("Please install it manually and run setup again.")
        return
    
    print("\n" + "=" * 60)
    print("SETUP COMPLETE!")
    print("=" * 60)
    
    print("\nYou can now run:")
    print("1. Original maze solver:")
    print("   python maze.py maze.txt")
    print("\n2. Interactive pathfinding game:")
    print("   python pathfinding_game.py")
    print("\n3. Demo script:")
    print("   python demo_search.py")
    
    print("\nFor more information, see README.md")

if __name__ == "__main__":
    main() 