# Git Commit Message Hook

This project enforces a specific commit message format using a git hook.

## 📋 Required Format

**All commits must follow this exact format:**

```
[ADD] commit description
```
or
```
[FEAT] commit description
```

## ✅ Valid Examples

```bash
git commit -m "[ADD] user authentication system"
git commit -m "[FEAT] stock data caching functionality"
git commit -m "[ADD] input validation for stock IDs"
git commit -m "[FEAT] real-time data updates"
git commit -m "[ADD] error handling for API requests"
git commit -m "[FEAT] automated report generation"
```

## ❌ Invalid Examples (Will be blocked)

```bash
git commit -m "add user authentication"        # Missing [ADD]/[FEAT]
git commit -m "feat: add feature"             # Wrong format
git commit -m "[add] something"               # Lowercase
git commit -m "[FEATURE] something"           # Wrong prefix
git commit -m "[ADD]something"                # Missing space
```

## 🚀 Usage

### Normal Workflow:
```bash
git add .
git commit -m "[ADD] your description here"
git push
```

### If Commit is Blocked:
1. Check the error message for the exact format required
2. Modify your commit message to use `[ADD]` or `[FEAT]`
3. Try committing again

### Emergency Bypass (Use sparingly):
```bash
git commit --no-verify -m "emergency fix"
```

## 🔧 Rules

1. **Prefix**: Must use `[ADD]` or `[FEAT]` (uppercase, in square brackets)
2. **Space**: Must have a space after the closing bracket
3. **Description**: At least 3 characters after the prefix
4. **Length**: Maximum 100 characters total
5. **Period**: Don't end with a period

## 💡 When to Use Each Prefix

- **`[ADD]`**: Adding new functionality, files, features, or components
- **`[FEAT]`**: Major features or significant enhancements

## 🛠️ Hook Status

- ✅ **commit-msg hook**: Active (validates commit message format)
- ❌ **pre-commit hook**: Disabled (removed)  
- ❌ **pre-push hook**: Disabled (removed)

The hook will automatically check your commit message format and block commits that don't match the required pattern.