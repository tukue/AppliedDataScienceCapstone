"""Configuration management for the project."""
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR / "external"
MODELS_DIR = PROJECT_ROOT / "models"
LOGS_DIR = PROJECT_ROOT / "logs"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
REPORTS_DIR = PROJECT_ROOT / "reports"


def ensure_directories() -> None:
    """Create project directories used by local workflows."""
    for dir_path in [
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
        EXTERNAL_DATA_DIR,
        MODELS_DIR,
        LOGS_DIR,
        REPORTS_DIR,
    ]:
        dir_path.mkdir(parents=True, exist_ok=True)


def display_path(path: Path) -> str:
    """
    Return a reviewer-friendly path for logs and notebook output.

    Args:
        path: File or directory path

    Returns:
        Project-relative path when possible, otherwise only the path name
    """
    try:
        return path.resolve().relative_to(PROJECT_ROOT.resolve()).as_posix()
    except ValueError:
        return path.name


# Data configuration
SPACEX_API_URL = "https://api.spacexdata.com/v4"
TEST_SIZE = 0.2
RANDOM_STATE = 42
CV_FOLDS = 5

# Model configuration
MODEL_RANDOM_STATE = 42
VALIDATION_SIZE = 0.2

# Logging configuration
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = "INFO"
LOG_TO_CONSOLE = False
