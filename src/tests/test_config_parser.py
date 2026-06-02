from pathlib import Path

from app.conf_parser.parser import parse_config
from app.config import config as default_config

TEST_ENCODING = "utf-8"
REPORT_SIZE = 42


def test_parser_reads_config_values(tmp_path: Path) -> None:
    config_file = tmp_path / "config.txt"
    config_file.write_text(
        "# comment\nREPORT_SIZE = 42\nREPORT_DIR = ./reports\nLOG_DIR = ./logs\nLOG_FILE = ./app.log\n",
        encoding=TEST_ENCODING,
    )

    parsed_config = parse_config(config_file)

    assert parsed_config["REPORT_SIZE"] == REPORT_SIZE
    assert parsed_config["REPORT_DIR"] == "./reports"
    assert parsed_config["LOG_DIR"] == "./logs"
    assert parsed_config["LOG_FILE"] == "./app.log"


def test_parser_uses_defaults_for_missing_values(tmp_path: Path) -> None:
    config_file = tmp_path / "config.txt"
    config_file.write_text("REPORT_DIR = ./custom_reports\n", encoding=TEST_ENCODING)

    parsed_config = parse_config(config_file)

    assert parsed_config["REPORT_SIZE"] == default_config["REPORT_SIZE"]
    assert parsed_config["REPORT_DIR"] == "./custom_reports"
    assert parsed_config["LOG_DIR"] == default_config["LOG_DIR"]
    assert "LOG_FILE" not in parsed_config
