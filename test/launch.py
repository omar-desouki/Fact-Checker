#!/usr/bin/env python3
"""
Enhanced RAG Fact Checker Launcher
Automated setup and launch script
"""

import os
import sys
import subprocess
import platform


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required.")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True


def check_dependencies():
    """Check and install dependencies if needed."""
    required_packages = ["gradio", "google-genai", "requests"]
    missing_packages = []

    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is missing")

    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", *missing_packages]
            )
            print("✅ All dependencies installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies.")
            print("   Please run: pip install -r requirements.txt")
            return False

    return True


def check_api_key():
    """Check if API key is configured."""
    if os.getenv("GOOGLE_API_KEY"):
        print("✅ Google API key found in environment")
        return True

    # Check if config file exists
    if os.path.exists("config.py"):
        try:
            import config

            if (
                hasattr(config, "GOOGLE_API_KEY")
                and config.GOOGLE_API_KEY != "your-google-api-key-here"
            ):
                print("✅ Google API key found in config.py")
                return True
        except ImportError:
            pass

    print("⚠️  Google API key not found!")
    print("   Please either:")
    print("   1. Set environment variable: export GOOGLE_API_KEY='your-key'")
    print("   2. Copy config_template.py to config.py and add your key")
    print("   3. Edit fact-checker.py directly")
    return False


def main():
    """Main launcher function."""
    print("🚀 Enhanced RAG Fact Checker Launcher")
    print("=" * 50)

    # Check system requirements
    if not check_python_version():
        sys.exit(1)

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    # Check API key
    api_key_ok = check_api_key()

    print("\n" + "=" * 50)
    if api_key_ok:
        print("🎉 All checks passed! Starting application...")
        print("🌐 Interface will be available at: http://localhost:7860")
        print("⏹️  Press Ctrl+C to stop the application")
        print("=" * 50)

        # Launch the application
        try:
            from fact_checker import main as app_main

            app_main()
        except KeyboardInterrupt:
            print("\n👋 Application stopped by user")
        except Exception as e:
            print(f"\n❌ Error starting application: {e}")
    else:
        print("⚠️  Please configure API key before running the application")
        sys.exit(1)


if __name__ == "__main__":
    main()
