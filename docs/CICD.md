# CI/CD Pipeline Documentation

## Overview

This project uses **GitHub Actions** for continuous integration and continuous deployment (CI/CD). The pipeline automatically runs tests, checks code quality, and validates security on every push and pull request.

## Workflows

### 1. **Tests & Code Quality** (`tests.yml`)
Runs on every push and pull request to main/develop branches, plus daily at 2 AM UTC.

**Jobs:**
- **Tests** - Run pytest with coverage (Python 3.11)
- **Code Quality** - Black formatting, Flake8 linting, mypy type checking
- **Security** - Bandit security scan, dependency vulnerability checks
- **Build** - Package building and validation
- **Notify** - Overall workflow status

**What it checks:**
✅ Unit tests pass (12+ test cases)
✅ Code coverage (generates reports)
✅ Code formatting (Black)
✅ Linting issues (Flake8)
✅ Type safety (mypy)
✅ Security vulnerabilities (Bandit)
✅ Dependency vulnerabilities (safety)
✅ Package builds correctly

**Artifacts:**
- Coverage reports (Codecov)
- Build artifacts (.whl, .tar.gz)

### 2. **Documentation** (`docs.yml`)
Runs when documentation files change.

**Jobs:**
- **Check Documentation** - Validate markdown, check API docs
- **API Docs Validation** - Extract and validate documented functions

**What it checks:**
✅ All markdown files are valid
✅ API documentation exists
✅ Documentation structure is correct
✅ Function documentation is complete

## Status Badges

Add these to your README.md:

```markdown
[![Tests & Code Quality](https://github.com/tukue/AppliedDataScienceCapstone/actions/workflows/tests.yml/badge.svg)](https://github.com/tukue/AppliedDataScienceCapstone/actions/workflows/tests.yml)
[![Documentation](https://github.com/tukue/AppliedDataScienceCapstone/actions/workflows/docs.yml/badge.svg)](https://github.com/tukue/AppliedDataScienceCapstone/actions/workflows/docs.yml)
[![codecov](https://codecov.io/gh/tukue/AppliedDataScienceCapstone/branch/main/graph/badge.svg)](https://codecov.io/gh/tukue/AppliedDataScienceCapstone)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
```

## Workflow Details

### Test Job
```yaml
- Runs pytest with coverage reporting
- Generates coverage.xml for Codecov
- Shows coverage gaps by line
- Uploads artifacts to Codecov
- Supports multiple Python versions in matrix (currently: 3.11)
```

### Code Quality Job
```yaml
- Black: Ensures consistent code formatting
- Flake8: Checks for style and logical errors
- mypy: Type checking for type safety
- Fails on format violations (blocking)
- Warnings on style issues (non-blocking)
```

### Security Job
```yaml
- Bandit: Finds common security issues
- safety: Checks for known vulnerabilities in dependencies
- Non-blocking (informational)
```

### Build Job
```yaml
- Creates distribution packages (.whl, .tar.gz)
- Validates package contents
- Stores artifacts for 7 days
- Used for deployment or release testing
```

## Configuration

### Triggers

**On push:** main, develop branches
**On PR:** Against main, develop branches
**Scheduled:** Daily at 2 AM UTC (optional)

To disable scheduled runs, comment out the schedule section in `.yml` files.

### Python Version

Currently set to **Python 3.11** (stable, latest features).

To change:
```yaml
# In tests.yml
- uses: actions/setup-python@v4
  with:
    python-version: '3.10'  # Change here
```

### Coverage Thresholds

Currently set to upload all coverage reports without failing on thresholds.

To add threshold enforcement:
```yaml
- run: coverage report --fail-under=80
```

## Local Testing Before Push

Run these commands locally before pushing:

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/ -v --cov=src --cov-report=term-missing

# Format code
black src/ tests/

# Lint
flake8 src/ tests/

# Type check
mypy src/
```

**Tip:** Use pre-commit hooks to automate this:
```bash
pip install pre-commit
# Create .pre-commit-config.yaml to run these automatically
```

## Viewing Workflow Results

### In GitHub
1. Go to **Actions** tab in your repo
2. Click on a workflow run
3. See detailed logs for each job
4. Download artifacts if available

### Coverage Reports
- Upload to [Codecov.io](https://codecov.io) (recommended)
- Get detailed coverage visualization
- Track coverage over time

## Troubleshooting

### Tests Failing

**Check:**
1. Review test logs in Actions tab
2. Run locally: `pytest tests/ -v`
3. Check Python version: `python --version`
4. Verify dependencies: `pip install -r requirements-dev.txt`

### Code Quality Failing

**For Black:**
```bash
# Auto-fix formatting
black src/ tests/
git add -A
git commit -m "Format code with black"
git push
```

**For Flake8:**
Review the error messages and fix issues in your code.

**For mypy:**
Add type hints or use `# type: ignore` comments where necessary.

### Security Warnings

Review Bandit and safety output. Most are informational.

## Performance

### Expected Run Times
- Tests: 30-45 seconds
- Code Quality: 20-30 seconds
- Security: 15-20 seconds
- Build: 20-30 seconds
- **Total:** ~2-3 minutes

### Optimization Tips
- Tests run in parallel (when matrix is used)
- Dependencies cached between runs
- Artifacts automatically cleaned up after 7 days

## Best Practices

✅ **Always wait for CI to pass before merging**
✅ **Fix CI failures before pushing more commits**
✅ **Run tests locally first (faster feedback)**
✅ **Keep coverage high (aim for >80%)**
✅ **Review workflow logs for details**
✅ **Update workflows if dependencies change**

## Future Enhancements

Consider adding:
- [ ] Pre-commit hooks for local validation
- [ ] Auto-deployment on tags
- [ ] Scheduled dependency updates
- [ ] Performance benchmarking
- [ ] Documentation deployment
- [ ] Coverage trend tracking
- [ ] Code complexity analysis

## Useful Commands

```bash
# View workflow status
gh workflow list
gh workflow view tests.yml

# Trigger workflow manually
gh workflow run tests.yml

# View latest run
gh run list --workflow=tests.yml --limit 1

# Download artifacts
gh run download <RUN_ID>
```

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Pytest Documentation](https://docs.pytest.org/)
- [Black Code Formatter](https://black.readthedocs.io/)
- [Flake8 Linter](https://flake8.pycqa.org/)
- [mypy Type Checker](https://mypy.readthedocs.io/)
- [Codecov](https://codecov.io/)

---

**Status:** ✅ CI/CD Pipeline Active
**Last Updated:** July 3, 2026
