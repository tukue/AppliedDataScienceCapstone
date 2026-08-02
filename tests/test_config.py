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


def test_display_path_returns_project_relative_path(tmp_path, monkeypatch):
    """Test project paths are shown without local user folders."""
    project_root = tmp_path / "project"
    artifact_path = project_root / "models" / "model.joblib"
    monkeypatch.setattr(config, "PROJECT_ROOT", project_root)

    assert config.display_path(artifact_path) == "models/model.joblib"


def test_display_path_hides_external_absolute_path(tmp_path, monkeypatch):
    """Test external paths fall back to a non-identifying file name."""
    project_root = tmp_path / "project"
    external_path = tmp_path / "private-user-folder" / "analysis.log"
    monkeypatch.setattr(config, "PROJECT_ROOT", project_root)

    assert config.display_path(external_path) == "analysis.log"
