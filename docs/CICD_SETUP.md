# CI/CD Setup & Usage Guide

## Overview

This project includes a complete CI/CD pipeline using **GitHub Actions**. Automated testing and code quality checks run on every push and pull request.

## Quick Setup

### 1. Verify GitHub Actions are Enabled
- Go to your GitHub repository
- Click **Settings** → **Actions** → **General**
- Ensure "Allow all actions and reusable workflows" is selected

### 2. Set Up Codecov (Optional but Recommended)

For coverage reports:
1. Go to [codecov.io](https://codecov.io)
2. Sign in with GitHub
3. Add your repository
4. Codecov will automatically detect coverage reports from GitHub Actions

## Workflow Files

### 1. `.github/workflows/tests.yml`
**Main CI/CD pipeline for testing and code quality**

Runs on:
- Every push to `main` or `develop` branches
- Every pull request to `main` or `develop` branches
- Daily at 2 AM UTC

Jobs:
- `tests` - Run pytest with coverage
- `code-quality` - Black, Flake8, mypy checks
- `security` - Bandit and dependency vulnerability scans
- `build` - Package building and validation
- `notify` - Overall status notification

### 2. `.github/workflows/docs.yml`
**Documentation validation**

Runs when:
- Documentation files change (docs/, README.md)
- Pull requests affect documentation

Jobs:
- `check-documentation` - Markdown validation, structure check
- `api-docs-validation` - API documentation completeness

## Local Development

### Option 1: Run Tests Manually

```bash
# Single test run
pytest tests/

# With coverage
pytest tests/ --cov=src --cov-report=html

# Verbose output
pytest tests/ -v

# Specific test file
pytest tests/test_models.py
```

### Option 2: Use Pre-commit Hooks (Recommended)

Automatically runs checks before each commit:

```bash
# Install pre-commit
pip install pre-commit

# Set up hooks
pre-commit install

# Run on all files
pre-commit run --all-files
```

**This will:**
- ✅ Auto-format code with Black
- ✅ Check formatting issues
- ✅ Lint with Flake8
- ✅ Type check with mypy
- ✅ Fix trailing whitespace
- ✅ Check for large files

After setup, hooks run automatically before each commit!

## Common Tasks

### Before Pushing Code

```bash
# 1. Run tests locally
pytest tests/ -v

# 2. Format code
black src/ tests/

# 3. Lint
flake8 src/ tests/

# 4. Type check
mypy src/

# 5. Push
git push
```

**Tip:** Use pre-commit hooks to automate steps 2-4!

### If CI/CD Fails

#### Test Failures
```bash
# Run tests locally to debug
pytest tests/ -v

# Run specific failing test
pytest tests/test_models.py::TestModelTrainer::test_training -v

# Get detailed output
pytest tests/ -vv --tb=long
```

#### Code Format Issues
```bash
# Auto-fix with Black
black src/ tests/

# Commit and push
git add -A
git commit -m "Format code with black"
git push
```

#### Type Errors
Add type hints to fix mypy errors:
```python
# Before
def my_function(x):
    return x + 1

# After
def my_function(x: int) -> int:
    return x + 1
```

Or ignore specific lines:
```python
result = some_function()  # type: ignore
```

## Viewing CI/CD Results

### In GitHub Web Interface
1. Go to your repository
2. Click **Actions** tab
3. Click on a workflow run
4. View detailed logs for each job
5. Download artifacts

### Coverage Reports
- Reports are automatically uploaded to Codecov
- View at: `https://codecov.io/gh/username/AppliedDataScienceCapstone`
- Trend tracking available
- Badge available for README

### Build Artifacts
- Build artifacts stored for 7 days
- Download from GitHub Actions page
- Useful for testing before release

## Badges

Add these to your README.md to show CI/CD status:

```markdown
[![Tests & Code Quality](https://github.com/tukue/AppliedDataScienceCapstone/actions/workflows/tests.yml/badge.svg)](https://github.com/tukue/AppliedDataScienceCapstone/actions/workflows/tests.yml)
[![Documentation](https://github.com/tukue/AppliedDataScienceCapstone/actions/workflows/docs.yml/badge.svg)](https://github.com/tukue/AppliedDataScienceCapstone/actions/workflows/docs.yml)
[![codecov](https://codecov.io/gh/tukue/AppliedDataScienceCapstone/branch/main/graph/badge.svg)](https://codecov.io/gh/tukue/AppliedDataScienceCapstone)
```

## Customization

### Change Python Version
Edit `.github/workflows/tests.yml`:
```yaml
- uses: actions/setup-python@v4
  with:
    python-version: '3.10'  # Change here
```

### Add Coverage Thresholds
Edit `.github/workflows/tests.yml`:
```yaml
- run: pytest tests/ -v --cov=src --cov-report=xml --cov-fail-under=80
```

### Disable Scheduled Runs
In `.github/workflows/tests.yml`, comment out:
```yaml
# schedule:
#   - cron: '0 2 * * *'
```

### Add More Jobs
Edit workflow files to add additional checks:
- Performance benchmarking
- Code complexity analysis
- Documentation building
- Auto-deployment

## Debugging Workflows

### View Workflow Logs
1. Actions tab → Click failing run
2. Click on failed job
3. Expand steps to see logs
4. Look for error messages

### Enable Debug Logging
Add to workflow:
```yaml
env:
  ACTIONS_STEP_DEBUG: true
```

### Test Locally
Install and run locally before pushing:
```bash
# Test the exact command that runs in CI
pip install -r requirements-dev.txt
pytest tests/ -v --cov=src --cov-report=xml
```

## Best Practices

✅ **Run tests locally before pushing**
✅ **Use pre-commit hooks for automation**
✅ **Keep coverage high (>80%)**
✅ **Fix CI failures immediately**
✅ **Review workflow logs for details**
✅ **Update dependencies regularly**
✅ **Document any skipped tests**

❌ **Don't ignore CI failures**
❌ **Don't commit without running tests**
❌ **Don't skip linting checks**
❌ **Don't merge with failing CI**

## Performance

**Expected run times:**
- Tests: 30-45 seconds
- Code Quality: 20-30 seconds
- Security: 15-20 seconds
- Build: 20-30 seconds
- **Total: ~2-3 minutes**

**Tips to optimize:**
- Use caching (already configured)
- Split jobs into separate workflows
- Use concurrent jobs where possible

## Troubleshooting

### CI/CD Not Running
**Check:**
- Workflows are in `.github/workflows/` directory
- File names end with `.yml` or `.yaml`
- GitHub Actions enabled in Settings
- Branch is `main` or `develop`

### Workflow File Syntax Error
**Check:**
- YAML indentation is correct (2 spaces)
- All quotes are matched
- No tabs (use spaces only)
- Validate at: https://www.yamllint.com/

### Codecov Not Updating
**Check:**
- Repository added to Codecov
- Coverage XML file generated
- Branch is public (private repos need token)

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Pytest Documentation](https://docs.pytest.org/)
- [Codecov Documentation](https://docs.codecov.io/)
- [Pre-commit Hooks](https://pre-commit.com/)
- [Black Code Formatter](https://black.readthedocs.io/)
- [Flake8 Linter](https://flake8.pycqa.org/)

## Next Steps

1. ✅ Review workflow files in `.github/workflows/`
2. ✅ Install pre-commit hooks: `pre-commit install`
3. ✅ Run tests locally: `pytest tests/`
4. ✅ Set up Codecov (optional)
5. ✅ Push to trigger CI/CD pipeline
6. ✅ Monitor Actions tab for results

---

**Status:** ✅ CI/CD Pipeline Ready
**Last Updated:** July 3, 2026
**Python Version:** 3.11
