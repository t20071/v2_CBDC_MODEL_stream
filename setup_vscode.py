#!/usr/bin/env python3
"""
Setup script for CBDC Banking Simulation in VS Code
Run this script to create all necessary configuration files
"""

import os
import sys

def create_requirements_txt():
    """Create requirements.txt with core dependencies"""
    requirements = [
        "streamlit>=1.45.1",
        "mesa>=3.2.0", 
        "plotly>=6.1.2",
        "pandas>=2.3.0",
        "numpy>=2.3.0",
        "networkx>=3.5"
    ]
    
    with open('requirements.txt', 'w') as f:
        f.write('\n'.join(requirements) + '\n')
    
    print("✓ Created requirements.txt")

def create_vscode_config():
    """Create VS Code configuration files"""
    os.makedirs('.vscode', exist_ok=True)
    
    # Launch configuration
    launch_config = """{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Streamlit App",
            "type": "python",
            "request": "launch",
            "module": "streamlit",
            "args": ["run", "app.py", "--server.port", "8501"],
            "console": "integratedTerminal",
            "justMyCode": true,
            "cwd": "${workspaceFolder}"
        }
    ]
}"""
    
    with open('.vscode/launch.json', 'w') as f:
        f.write(launch_config)
    
    # Settings
    settings = """{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "files.associations": {
        "*.py": "python"
    },
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true
}"""
    
    with open('.vscode/settings.json', 'w') as f:
        f.write(settings)
    
    print("✓ Created VS Code configuration files")

def create_streamlit_config():
    """Ensure Streamlit configuration exists"""
    os.makedirs('.streamlit', exist_ok=True)
    
    config = """[server]
headless = true
address = "0.0.0.0"
port = 8501

[browser]
gatherUsageStats = false"""
    
    with open('.streamlit/config.toml', 'w') as f:
        f.write(config)
    
    print("✓ Created Streamlit configuration")

def create_run_scripts():
    """Create convenient run scripts"""
    
    # Windows batch file
    batch_script = """@echo off
echo Activating virtual environment...
call venv\\Scripts\\activate
echo Starting CBDC Banking Simulation...
streamlit run app.py
pause"""
    
    with open('run_windows.bat', 'w') as f:
        f.write(batch_script)
    
    # Unix shell script
    shell_script = """#!/bin/bash
echo "Activating virtual environment..."
source venv/bin/activate
echo "Starting CBDC Banking Simulation..."
streamlit run app.py"""
    
    with open('run_unix.sh', 'w') as f:
        f.write(shell_script)
    
    # Make shell script executable
    os.chmod('run_unix.sh', 0o755)
    
    print("✓ Created run scripts (run_windows.bat and run_unix.sh)")

def main():
    print("Setting up CBDC Banking Simulation for VS Code...")
    print("=" * 50)
    
    create_requirements_txt()
    create_vscode_config()
    create_streamlit_config()
    create_run_scripts()
    
    print("\n" + "=" * 50)
    print("Setup complete! Next steps:")
    print("1. Create virtual environment: python -m venv venv")
    print("2. Activate it:")
    print("   - Windows: venv\\Scripts\\activate")
    print("   - macOS/Linux: source venv/bin/activate")
    print("3. Install dependencies: pip install -r requirements.txt")
    print("4. Run the app: streamlit run app.py")
    print("\nOr use the convenience scripts:")
    print("- Windows: run_windows.bat")
    print("- macOS/Linux: ./run_unix.sh")

if __name__ == "__main__":
    main()