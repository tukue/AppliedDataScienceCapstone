# Contributing Guide

## Overview

This project follows data science best practices. All contributions should maintain code quality, documentation, and reproducibility.

## Development Setup

1. Clone the repository and create a virtual environment:
```bash
git clone git@github.com:tukue/AppliedDataScienceCapstone.git
cd AppliedDataScienceCapstone
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install development dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

3. Verify setup:
```bash
pytest tests/
```

## Code Quality

### Style Guide
- Follow PEP 8
- Use type hints in function signatures
- Write docstrings for all functions and classes
- Maximum line length: 100 characters

### Formatting
Format code with Black:
```bash
black src/ tests/
```

### Linting
Check code quality with Flake8:
```bash
flake8 src/ tests/
```

### Type Checking
Run type checks with mypy:
```bash
mypy src/
```

## Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_models.py

# Run with verbose output
pytest -v
```

### Writing Tests
- Place tests in `tests/` directory
- Name test files `test_*.py`
- Use pytest fixtures for setup
- Aim for >80% code coverage

Example:
```python
def test_my_function():
    """Test description."""
    result = my_function(input_data)
    assert result == expected_output
```

## Documentation

### Docstring Format
Use Google-style docstrings:

```python
def my_function(param1: str, param2: int) -> bool:
    """
    Short description.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Example:
        >>> result = my_function("hello", 42)
        >>> print(result)
        True
    """
    pass
```

### Comments
- Only comment code that needs clarification
- Explain WHY, not WHAT
- Keep comments up-to-date with code

## Module Organization

### Adding New Features

1. **Create module in appropriate location:**
   - Data operations: `src/data/`
   - Feature engineering: `src/features/`
   - Model operations: `src/models/`

2. **Add function with docstring:**
   ```python
   def new_function(param: type) -> return_type:
       """Description."""
       # Implementation
       return result
   ```

3. **Add logging:**
   ```python
   from src.logger import setup_logger
   
   logger = setup_logger(__name__)
   logger.info("Descriptive message")
   ```

4. **Write tests:**
   ```bash
   # Create test_new_function in appropriate test file
   pytest tests/
   ```

5. **Update documentation:**
   - Add to `docs/API.md`
   - Update function examples

## Notebook Guidelines

### For Original Notebooks
- Keep in `notebooks/original/` (preserved as-is)
- All graphs and outputs preserved
- Used as reference for refactoring

### For New Analysis Notebooks
- Create in `notebooks/exploratory/`
- Use modular code from `src/`
- Generate and save figures to `notebooks/figures/`
- Keep notebooks clean and reproducible

Example notebook structure:
```python
# 1. Imports
from src.data import fetch_spacex_launches
from src.logger import setup_logger

# 2. Setup
logger = setup_logger(__name__)

# 3. Load Data
data = fetch_spacex_launches()

# 4. Analysis
# ... your analysis ...

# 5. Visualization
# ... save figures ...
```

## Git Workflow

### Branch Naming
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation
- `refactor/` - Refactoring

Example: `feature/data-validation`

### Commit Messages
- Use clear, descriptive messages
- Start with action verb (Add, Fix, Update, etc.)
- Reference issues if applicable

Examples:
- "Add data validation function"
- "Fix missing value handling in preprocessing"
- "Update API documentation"

### Pull Requests
- Link related issues
- Describe changes clearly
- Ensure tests pass
- Request review from maintainers

## Reporting Issues

### Bug Reports
Include:
- Description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Python/package versions
- Error traceback

### Feature Requests
Include:
- Use case/motivation
- Proposed solution
- Alternative approaches
- Examples

## Contact

For questions or discussions:
- Open an issue on GitHub
- Check existing issues/discussions first

## Code of Conduct

- Be respectful and inclusive
- Welcome diverse perspectives
- Keep discussions constructive
- Report inappropriate behavior

---

Thank you for contributing to this project!
