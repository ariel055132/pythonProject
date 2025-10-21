# Git Hooks Documentation

This document explains the git hooks implementation for the Taiwan Stock Info project, designed to maintain code quality and enforce best practices.

## 🎯 Overview

Git hooks are scripts that run automatically at certain points in the Git workflow. They help maintain code quality, enforce standards, and prevent issues from entering the repository.

## 🔧 Installed Hooks

### 1. Pre-commit Hook (`pre-commit`)

**Runs before each commit to check code quality**

**What it checks:**
- ✅ Python syntax errors
- ✅ Code style with flake8 (if available)
- ✅ Import sorting with isort (if available)
- ✅ Basic SOLID principles violations
- ✅ Function length (SRP violations)
- ✅ Too many imports (coupling issues)
- ✅ Bare except clauses

**Example output:**
```
🚀 Running pre-commit checks...
==================================================
🔍 Checking Python syntax...
✅ Python syntax check passed

🎨 Checking code style...
✅ Code style check passed

📦 Checking import sorting...
✅ Import sorting check passed

🏗️  Checking SOLID principles (basic)...
✅ SOLID principles check passed

==================================================
✅ All pre-commit checks passed! 🎉
```

### 2. Commit Message Hook (`commit-msg`)

**Validates commit message format and enforces good practices**

**Supported formats:**
1. **Conventional Commits:** `type(scope): description`
2. **Traditional:** `Capitalized imperative description`

**Validation rules:**
- ✅ Minimum 10 characters
- ✅ Maximum 72 characters for subject line
- ✅ Proper format (conventional or traditional)
- ✅ No period at end of subject line
- ✅ Imperative mood for traditional format
- ✅ Lowercase start for conventional commits
- ❌ Blocks WIP, temp, debug commits

**Examples of good commit messages:**
```bash
# Conventional Commits
feat: add user authentication system
fix: resolve memory leak in data processing
docs: update API documentation for v2.0
refactor: extract validation logic to separate module
test: add unit tests for stock data service

# Traditional Format
Add user authentication system
Fix memory leak in data processing
Update API documentation for v2.0
Extract validation logic to separate module
Add unit tests for stock data service
```

### 3. Pre-push Hook (`pre-push`)

**Runs before pushing to remote repository to ensure code quality**

**What it checks:**
- 🔍 Python syntax for all files
- 🧪 Runs all tests (pytest or unittest)
- 🌿 Warns when pushing to protected branches
- 🔬 Optional static analysis (mypy, bandit)

**Protected branches:** main, master, production, release

**Example output:**
```
🚀 Running pre-push checks...
==================================================
Running Branch protection...
✅ Pushing to branch: feature/new-functionality

Running Python syntax...
✅ All Python files have valid syntax

Running Tests...
🧪 Running Python tests...
   Using pytest...
✅ All pytest tests passed

Running Static analysis...
🔬 Running static analysis...
   Running mypy type checking...
   Running bandit security analysis...

==================================================
✅ All pre-push checks passed! 🚀
   Your code is ready to be pushed.
```

## 🚀 Usage

### Automatic Usage
Hooks run automatically during normal Git operations:

```bash
# Pre-commit hook runs automatically
git commit -m "feat: add new feature"

# Pre-push hook runs automatically  
git push origin main
```

### Manual Testing
You can run hooks manually for testing:

```bash
# Test pre-commit hook
.git/hooks/pre-commit

# Test commit message validation
echo "feat: test message" > .git/COMMIT_EDITMSG
.git/hooks/commit-msg .git/COMMIT_EDITMSG

# Test pre-push hook
.git/hooks/pre-push
```

### Bypassing Hooks (Emergency Only)
```bash
# Skip pre-commit and commit-msg hooks
git commit --no-verify -m "emergency fix"

# Skip pre-push hook
git push --no-verify
```

## ⚙️ Setup and Configuration

### Quick Setup
Run the setup script to install everything:

```bash
python setup_hooks.py
```

### Manual Setup
1. **Install development dependencies:**
   ```bash
   pip install flake8 isort pytest mypy bandit black
   ```

2. **Make hooks executable:**
   ```bash
   chmod +x .git/hooks/pre-commit
   chmod +x .git/hooks/commit-msg
   chmod +x .git/hooks/pre-push
   ```

3. **Create configuration files:**
   - `.flake8` - Code style configuration
   - `pyproject.toml` - Tool configuration
   - `pytest.ini` - Test configuration

### Configuration Files

#### `.flake8`
```ini
[flake8]
max-line-length = 100
ignore = E203, W503, F401
exclude = .git, __pycache__, venv, build, dist
```

#### `pyproject.toml`
```toml
[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 100

[tool.black]
line-length = 100
target-version = ['py38']

[tool.mypy]
python_version = "3.8"
warn_return_any = true
ignore_missing_imports = true
```

## 🧪 Testing Strategy

### Pre-commit Testing
The pre-commit hook tests:
- All staged Python files for syntax
- Code style compliance
- Import organization
- Basic architecture violations

### Pre-push Testing
The pre-push hook runs:
- Full test suite (pytest or unittest)
- Syntax check for all Python files
- Static analysis (optional)

### Recommended Test Structure
```
tests/
├── test_models/
│   ├── test_stock_request.py
├── test_services/
│   ├── test_stock_service.py
├── test_clients/
│   ├── test_taiwan_stock_client.py
└── test_utils/
    ├── test_request_utils.py
    └── test_csv_utils.py
```

## 🔧 Troubleshooting

### Common Issues

#### Hook Permission Errors
```bash
# Fix permission issues
chmod +x .git/hooks/*
```

#### Missing Dependencies
```bash
# Install all development dependencies
pip install flake8 isort pytest mypy bandit black
```

#### Hook Not Running
```bash
# Check if hook exists and is executable
ls -la .git/hooks/pre-commit
```

#### Syntax Errors in Hooks
```bash
# Test hook syntax
python .git/hooks/pre-commit
```

### Hook Customization

#### Disable Specific Checks
Edit the hook files to comment out unwanted checks:

```python
# In .git/hooks/pre-commit
checks = [
    check_python_syntax,
    # check_code_style,  # Disable style checking
    check_imports,
    check_solid_principles,
]
```

#### Add Custom Checks
Add new validation functions to the hooks:

```python
def check_custom_rule():
    """Add your custom validation logic here."""
    print("🔍 Running custom check...")
    # Your validation logic
    return True  # or False if check fails

# Add to checks list
checks = [
    # ... existing checks
    check_custom_rule,
]
```

## 📊 Benefits

### Code Quality
- ✅ Prevents syntax errors from being committed
- ✅ Enforces consistent code style
- ✅ Catches basic architecture violations
- ✅ Maintains organized imports

### Team Collaboration
- ✅ Consistent commit message format
- ✅ Shared code quality standards
- ✅ Automated testing before sharing code
- ✅ Reduced code review overhead

### Productivity  
- ✅ Catch issues early in development
- ✅ Reduce CI/CD pipeline failures
- ✅ Faster feedback loop
- ✅ Less time debugging in production

## 🔄 Alternative: Pre-commit Framework

For more advanced hook management, consider the [pre-commit framework](https://pre-commit.com/):

```bash
# Install pre-commit framework
pip install pre-commit

# Run setup script and choose "yes" for pre-commit framework
python setup_hooks.py
```

The pre-commit framework provides:
- Standardized hook management
- Easy configuration via YAML
- Large ecosystem of pre-built hooks
- Automatic hook updates

## 📝 Best Practices

### Commit Messages
1. Use conventional commits for better Git history
2. Keep subject line under 72 characters
3. Use imperative mood ("Add" not "Added")
4. Separate subject from body with blank line

### Code Quality
1. Fix all hook violations before committing
2. Run tests locally before pushing
3. Use meaningful variable and function names
4. Follow SOLID principles in design

### Hook Management
1. Keep hooks fast (under 10 seconds)
2. Provide clear error messages
3. Make hooks skippable for emergencies
4. Document any custom modifications

## 🆘 Support

If you encounter issues with the git hooks:

1. **Check the hook output** for specific error messages
2. **Run hooks manually** to debug issues
3. **Verify dependencies** are installed correctly
4. **Check file permissions** on hook scripts
5. **Use `--no-verify`** flag for emergency commits

Remember: Hooks are tools to help maintain quality, not barriers to productivity!