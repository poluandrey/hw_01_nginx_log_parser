from pathlib import Path

import pytest

from app.main import DEFAULT_CONFIG_PATH, PROJECT_DESCRIPTION, parse_args

TEST_ENCODING = "utf-8"
CONFIG_OPTION = "--config"


def test_parse_args_returns_existing_config_path(tmp_path: Path) -> None:
    config_file = tmp_path / "config.yml"
    config_file.write_text("version: 1\n", encoding=TEST_ENCODING)

    parsed_args = parse_args([CONFIG_OPTION, str(config_file)])

    assert parsed_args.config == config_file


def test_parse_args_exits_on_missing_config() -> None:
    with pytest.raises(SystemExit):
        parse_args([CONFIG_OPTION, "missing.yml"])


def test_parse_args_uses_default_config_path() -> None:
    parsed_args = parse_args([])

    assert parsed_args.config == DEFAULT_CONFIG_PATH


def test_main_reraises_help_exit() -> None:
    with pytest.raises(SystemExit) as exc_info:
        parse_args(["--help"])

    assert exc_info.value.code == 0


def test_parser_description_mentions_project_goal() -> None:
    assert "Анализатор логов nginx" in PROJECT_DESCRIPTION
