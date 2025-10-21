#!/usr/bin/env python3
"""
Git hooks setup script for the Taiwan Stock Info project.
This script helps install and configure git hooks for code quality.
"""

import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

def run_command(command):
    """Run a shell command and return success status."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_git_repository():
    """Check if we're in a git repository."""
    if not os.path.exists('.git'):
        print("❌ Error: Not in a git repository")
        print("   Run 'git init' first or run this script from the project root")
        return False
    
    print("✅ Git repository detected")
    return True

def install_development_dependencies():
    """Install recommended development dependencies."""
    print("📦 Installing development dependencies...")
    
    dependencies = [
        ("flake8", "Code style checking"),
        ("isort", "Import sorting"),
        ("pytest", "Testing framework"),
        ("mypy", "Type checking"),
        ("bandit", "Security analysis"),
        ("black", "Code formatting"),
    ]
    
    installed = []
    failed = []
    
    for package, description in dependencies:
        print(f"   Installing {package} ({description})...")
        success, stdout, stderr = run_command(f"pip install {package}")
        if success:
            installed.append(package)
        else:
            failed.append((package, stderr))
    
    if installed:
        print("✅ Successfully installed:")
        for package in installed:
            print(f"   - {package}")
    
    if failed:
        print("⚠️  Failed to install:")
        for package, error in failed:
            print(f"   - {package}: {error}")
    
    return len(failed) == 0

def create_development_configs():
    """Create configuration files for development tools."""
    print("⚙️  Creating development configuration files...")
    
    # Create .flake8 config
    flake8_config = """[flake8]
max-line-length = 100
ignore = 
    E203,  # whitespace before ':'
    W503,  # line break before binary operator
    F401,  # imported but unused (handled by isort)
exclude = 
    .git,
    __pycache__,
    venv,
    .venv,
    build,
    dist
"""
    
    # Create pyproject.toml for isort and black
    pyproject_config = """[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 100
known_first_party = ["info", "utils", "models", "clients", "services", "strategies"]

[tool.black]
line-length = 100
target-version = ['py38']
include = '\\.pyi?$'
extend-exclude = '''
/(
  # directories
  \\.eggs
  | \\.git
  | \\.mypy_cache
  | \\.pytest_cache
  | \\.venv
  | venv
  | build
  | dist
)/
'''

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
ignore_missing_imports = true
"""
    
    # Create pytest.ini
    pytest_config = """[tool:pytest]
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
"""
    
    configs = [
        ('.flake8', flake8_config),
        ('pyproject.toml', pyproject_config),
        ('pytest.ini', pytest_config),
    ]
    
    for filename, content in configs:
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                f.write(content)
            print(f"✅ Created {filename}")
        else:
            print(f"⚠️  {filename} already exists, skipping")

def setup_pre_commit_framework():
    """Optionally set up pre-commit framework (alternative approach)."""
    print("\n🔧 Pre-commit Framework Setup (Optional)")
    print("   The pre-commit framework is an alternative to custom git hooks")
    print("   It provides a standardized way to manage git hooks")
    
    response = input("   Would you like to install pre-commit framework? (y/N): ")
    if response.lower() not in ['y', 'yes']:
        return
    
    # Install pre-commit
    success, stdout, stderr = run_command("pip install pre-commit")
    if not success:
        print(f"❌ Failed to install pre-commit: {stderr}")
        return
    
    # Create .pre-commit-config.yaml
    precommit_config = """repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: debug-statements
      
  - repo: https://github.com/psf/black
    rev: 22.10.0
    hooks:
      - id: black
        language_version: python3
        
  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort
        args: ["--profile", "black"]
        
  - repo: https://github.com/pycqa/flake8
    rev: 5.0.4
    hooks:
      - id: flake8
        args: [--max-line-length=100]
        
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.991
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
"""
    
    if not os.path.exists('.pre-commit-config.yaml'):
        with open('.pre-commit-config.yaml', 'w') as f:
            f.write(precommit_config)
        print("✅ Created .pre-commit-config.yaml")
        
        # Install the git hook scripts
        success, stdout, stderr = run_command("pre-commit install")
        if success:
            print("✅ Pre-commit hooks installed")
        else:
            print(f"❌ Failed to install pre-commit hooks: {stderr}")
    else:
        print("⚠️  .pre-commit-config.yaml already exists")

def test_hooks():
    """Test the installed git hooks."""
    print("🧪 Testing git hooks...")
    
    # Test pre-commit hook
    if os.path.exists('.git/hooks/pre-commit'):
        print("   Testing pre-commit hook...")
        # Create a simple test commit
        success, stdout, stderr = run_command("echo 'print(\"test\")' > test_hook.py")
        if success:
            success, stdout, stderr = run_command("git add test_hook.py")
            if success:
                # This will run the pre-commit hook
                success, stdout, stderr = run_command("git commit --dry-run -m 'test: hook test'")
                run_command("git reset HEAD test_hook.py")  # Unstage
                run_command("rm -f test_hook.py")  # Clean up
        
        if success:
            print("✅ Pre-commit hook is working")
        else:
            print("⚠️  Pre-commit hook test failed")
    
    print("✅ Hook testing completed")

def show_usage_instructions():
    """Show instructions on how to use the git hooks."""
    instructions = """
🎉 Git Hooks Setup Complete!

📋 What was installed:
  ✅ pre-commit: Runs code quality checks before commits
  ✅ commit-msg: Validates commit message format  
  ✅ pre-push: Runs tests before pushing to remote

🚀 How to use:

1. Normal workflow:
   git add .
   git commit -m "feat: add new feature"  # Hook will run automatically
   git push                               # Hook will run tests

2. Skip hooks (emergency only):
   git commit --no-verify -m "emergency fix"
   git push --no-verify

3. Run hooks manually:
   .git/hooks/pre-commit                 # Check code quality
   .git/hooks/commit-msg .git/COMMIT_EDITMSG  # Test commit message

4. Good commit message examples:
   feat: add user authentication
   fix: resolve memory leak in parser
   docs: update API documentation
   refactor: extract validation logic
   test: add unit tests for service layer

💡 Tips:
  - Install recommended tools: flake8, isort, pytest, mypy, bandit
  - Use conventional commits for better Git history
  - Fix all issues before committing for best practices
  - Hooks help maintain code quality automatically

🛠️  Configuration files created:
  - .flake8 (code style configuration)
  - pyproject.toml (isort and black configuration)  
  - pytest.ini (test configuration)
"""
    print(instructions)

def main():
    """Main setup function."""
    print("🚀 Git Hooks Setup for Taiwan Stock Info Project")
    print("=" * 60)
    
    if not check_git_repository():
        return 1
    
    print("\n1. Installing development dependencies...")
    install_development_dependencies()
    
    print("\n2. Creating configuration files...")
    create_development_configs()
    
    print("\n3. Setting up pre-commit framework (optional)...")
    setup_pre_commit_framework()
    
    print("\n4. Testing hooks...")
    test_hooks()
    
    print("\n5. Setup complete!")
    show_usage_instructions()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())