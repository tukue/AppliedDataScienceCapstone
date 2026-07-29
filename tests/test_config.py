"""Unit tests for project configuration helpers."""

import src.config as config


def test_ensure_directories_creates_expected_paths(tmp_path, monkeypatch):
    """Test explicit directory creation for local workflow outputs."""
    paths = {
        "RAW_DATA_DIR": tmp_path / "data" / "raw",
        "PROCESSED_DATA_DIR": tmp_path / "data" / "processed",
        "EXTERNAL_DATA_DIR": tmp_path / "data" / "external",
        "MODELS_DIR": tmp_path / "models",
        "LOGS_DIR": tmp_path / "logs",
        "REPORTS_DIR": tmp_path / "reports",
    }
    for name, path in paths.items():
        monkeypatch.setattr(config, name, path)

    config.ensure_directories()

    assert all(path.exists() and path.is_dir() for path in paths.values())
