#!/usr/bin/env python3
"""
Development Environment Setup Script for VITA Panel Testing

This script automates the setup of a complete development environment
following Python best practices and Scrum methodology principles.

Usage:
    python setup_dev_env.py [--python-version 3.11]
"""

import argparse
import os
import subprocess
import sys
import venv
from pathlib import Path
from typing import List, Optional


class VitaDevSetup:
    """Development environment setup automation for VITA project."""
    
    def __init__(self, python_version: str = "3.11"):
        """Initialize the development setup.
        
        Args:
            python_version: Target Python version for virtual environment
        """
        self.project_root = Path(__file__).parent
        self.venv_path = self.project_root / "vita_venv"
        self.python_version = python_version
        
    def run_command(self, cmd: List[str], check: bool = True) -> subprocess.CompletedProcess:
        """Execute a shell command with proper error handling.
        
        Args:
            cmd: Command to execute as list of strings
            check: Whether to raise exception on non-zero exit code
            
        Returns:
            CompletedProcess instance
            
        Raises:
            subprocess.CalledProcessError: If command fails and check=True
        """
        print(f"Running: {' '.join(cmd)}")
        try:
            result = subprocess.run(
                cmd, 
                check=check, 
                capture_output=True, 
                text=True,
                cwd=self.project_root
            )
            if result.stdout:
                print(result.stdout)
            return result
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {e}")
            if e.stderr:
                print(f"Error output: {e.stderr}")
            raise
    
    def check_python_version(self) -> bool:
        """Verify Python version meets minimum requirements.
        
        Returns:
            True if Python version is suitable
        """
        version_info = sys.version_info
        min_version = (3, 9)
        
        if version_info[:2] < min_version:
            print(f"Python {min_version[0]}.{min_version[1]}+ required. Found {version_info[0]}.{version_info[1]}")
            return False
        
        print(f"Python {version_info[0]}.{version_info[1]}.{version_info[2]} detected ✓")
        return True
    
    def create_virtual_environment(self) -> bool:
        """Create and activate virtual environment.
        
        Returns:
            True if virtual environment was created successfully
        """
        try:
            if self.venv_path.exists():
                print(f"Virtual environment already exists at {self.venv_path}")
                return True
                
            print(f"Creating virtual environment at {self.venv_path}")
            venv.create(self.venv_path, with_pip=True)
            
            # Verify virtual environment creation
            if self.venv_path.exists():
                print("Virtual environment created successfully ✓")
                return True
            else:
                print("Failed to create virtual environment ✗")
                return False
                
        except Exception as e:
            print(f"Error creating virtual environment: {e}")
            return False
    
    def get_pip_executable(self) -> Path:
        """Get the pip executable path for the virtual environment.
        
        Returns:
            Path to pip executable
        """
        if os.name == 'nt':  # Windows
            return self.venv_path / "Scripts" / "pip.exe"
        else:  # Unix-like
            return self.venv_path / "bin" / "pip"
    
    def install_dependencies(self) -> bool:
        """Install project and development dependencies.
        
        Returns:
            True if all dependencies were installed successfully
        """
        pip_exe = self.get_pip_executable()
        
        try:
            # Upgrade pip first
            print("Upgrading pip...")
            self.run_command([str(pip_exe), "install", "--upgrade", "pip"])
            
            # Install project dependencies
            print("Installing project dependencies...")
            requirements_file = self.project_root / "requirements.txt"
            if requirements_file.exists():
                self.run_command([str(pip_exe), "install", "-r", str(requirements_file)])
            
            # Install development dependencies
            print("Installing development dependencies...")
            dev_requirements_file = self.project_root / "dev-requirements.txt"
            if dev_requirements_file.exists():
                self.run_command([str(pip_exe), "install", "-r", str(dev_requirements_file)])
            
            # Install project in development mode if pyproject.toml exists
            pyproject_file = self.project_root / "pyproject.toml"
            if pyproject_file.exists():
                print("Installing project in development mode...")
                self.run_command([str(pip_exe), "install", "-e", ".[dev]"])
            
            print("Dependencies installed successfully ✓")
            return True
            
        except subprocess.CalledProcessError:
            print("Failed to install dependencies ✗")
            return False
    
    def setup_pre_commit(self) -> bool:
        """Install and configure pre-commit hooks.
        
        Returns:
            True if pre-commit was configured successfully
        """
        try:
            # Check if .pre-commit-config.yaml exists
            pre_commit_config = self.project_root / ".pre-commit-config.yaml"
            if not pre_commit_config.exists():
                print("No .pre-commit-config.yaml found, skipping pre-commit setup")
                return True
            
            # Get pre-commit executable from virtual environment
            if os.name == 'nt':  # Windows
                pre_commit_exe = self.venv_path / "Scripts" / "pre-commit.exe"
            else:  # Unix-like
                pre_commit_exe = self.venv_path / "bin" / "pre-commit"
            
            if not pre_commit_exe.exists():
                print("pre-commit not installed, skipping pre-commit setup")
                return False
            
            print("Installing pre-commit hooks...")
            self.run_command([str(pre_commit_exe), "install"])
            
            print("Pre-commit hooks installed successfully ✓")
            return True
            
        except subprocess.CalledProcessError:
            print("Failed to setup pre-commit hooks ✗")
            return False
    
    def create_project_structure(self) -> bool:
        """Create recommended project directory structure.
        
        Returns:
            True if project structure was created successfully
        """
        try:
            directories = [
                "src/vita",
                "tests/unit",
                "tests/integration",
                "tests/fixtures",
                "docs",
                "scripts",
                "config",
            ]
            
            for directory in directories:
                dir_path = self.project_root / directory
                dir_path.mkdir(parents=True, exist_ok=True)
                
                # Create __init__.py files for Python packages
                if "src/" in directory or directory == "tests":
                    init_file = dir_path / "__init__.py"
                    if not init_file.exists():
                        init_file.write_text("")
            
            print("Project structure created successfully ✓")
            return True
            
        except Exception as e:
            print(f"Failed to create project structure: {e} ✗")
            return False
    
    def generate_activation_scripts(self) -> None:
        """Generate convenient activation scripts for different platforms."""
        # Windows batch script
        windows_script = self.project_root / "activate_dev_env.bat"
        windows_content = f"""@echo off
echo Activating VITA development environment...
call {self.venv_path}\\Scripts\\activate.bat
echo Development environment activated!
echo.
echo Available commands:
echo   python -m pytest          : Run tests
echo   black src tests           : Format code
echo   flake8 src tests          : Lint code
echo   mypy src                  : Type checking
echo   pre-commit run --all-files: Run all pre-commit hooks
echo.
cmd /k
"""
        windows_script.write_text(windows_content)
        
        # Unix shell script
        unix_script = self.project_root / "activate_dev_env.sh"
        unix_content = f"""#!/bin/bash
echo "Activating VITA development environment..."
source {self.venv_path}/bin/activate
echo "Development environment activated!"
echo ""
echo "Available commands:"
echo "  python -m pytest          : Run tests"
echo "  black src tests           : Format code"
echo "  flake8 src tests          : Lint code"
echo "  mypy src                  : Type checking"
echo "  pre-commit run --all-files: Run all pre-commit hooks"
echo ""
exec bash
"""
        unix_script.write_text(unix_content)
        
        # Make Unix script executable
        if os.name != 'nt':
            os.chmod(unix_script, 0o755)
        
        print("Activation scripts created successfully ✓")
    
    def setup(self) -> bool:
        """Run the complete development environment setup.
        
        Returns:
            True if setup completed successfully
        """
        print("🚀 Setting up VITA development environment...")
        print("=" * 50)
        
        steps = [
            ("Checking Python version", self.check_python_version),
            ("Creating virtual environment", self.create_virtual_environment),
            ("Installing dependencies", self.install_dependencies),
            ("Creating project structure", self.create_project_structure),
            ("Setting up pre-commit hooks", self.setup_pre_commit),
        ]
        
        for step_name, step_func in steps:
            print(f"\n📋 {step_name}...")
            if not step_func():
                print(f"❌ Setup failed at: {step_name}")
                return False
        
        # Generate activation scripts (non-critical)
        print(f"\n📋 Generating activation scripts...")
        self.generate_activation_scripts()
        
        print("\n" + "=" * 50)
        print("✅ Development environment setup completed successfully!")
        print("\nNext steps:")
        print("1. Activate the environment:")
        if os.name == 'nt':
            print(f"   activate_dev_env.bat")
        else:
            print(f"   source activate_dev_env.sh")
        print("2. Run tests: python -m pytest")
        print("3. Check code quality: pre-commit run --all-files")
        print("4. Start development server: python vita_app.py")
        
        return True


def main():
    """Main entry point for the development environment setup."""
    parser = argparse.ArgumentParser(description="Setup VITA development environment")
    parser.add_argument(
        "--python-version", 
        default="3.11",
        help="Python version to use (default: 3.11)"
    )
    
    args = parser.parse_args()
    
    setup = VitaDevSetup(python_version=args.python_version)
    success = setup.setup()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()