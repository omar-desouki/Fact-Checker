@echo off
echo 🚀 Enhanced RAG Fact Checker - Windows Launcher
echo ================================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo    Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

REM Install dependencies if needed
echo 📦 Installing dependencies...
pip install gradio google-genai requests

REM Check if fact-checker.py exists
if not exist "fact-checker.py" (
    echo ❌ fact-checker.py not found in current directory
    pause
    exit /b 1
)

REM Launch the application
echo 🌐 Starting Enhanced RAG Fact Checker...
echo    Interface will be available at: http://localhost:7860
echo    Press Ctrl+C to stop the application
echo ================================================
python fact-checker.py

pause
