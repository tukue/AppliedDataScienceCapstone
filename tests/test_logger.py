"""Unit tests for project logging behavior."""

from src.logger import setup_logger


def test_logger_is_silent_by_default(capsys):
    """Test log messages do not pollute normal output by default."""
    logger = setup_logger("tests.silent_default")

    logger.info("this should not be printed")
    captured = capsys.readouterr()

    assert captured.out == ""
    assert captured.err == ""


def test_logger_console_output_is_opt_in(capsys):
    """Test console output is available when explicitly requested."""
    logger = setup_logger("tests.console_enabled", console=True)

    logger.info("visible log message")
    captured = capsys.readouterr()

    assert "visible log message" in captured.err


def test_logger_file_output_is_opt_in(tmp_path, monkeypatch):
    """Test file output works without writing to console."""
    import src.logger as logger_module

    monkeypatch.setattr(logger_module, "LOGS_DIR", tmp_path)
    logger = setup_logger("tests.file_enabled", log_file="analysis.log")

    logger.info("file log message")
    log_path = tmp_path / "analysis.log"

    assert log_path.exists()
    assert "file log message" in log_path.read_text()
