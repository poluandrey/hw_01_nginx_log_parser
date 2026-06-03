import argparse
from pathlib import Path

from app.analyzer import analyze
from app.conf_parser.parser import parse_config
from app.logger import configure_logger

PROJECT_DESCRIPTION = (
    "Анализатор логов nginx: сервис формирует статистический отчет "
    "о характеристиках запросов на основании парсинга логов."
)


def existing_file(file_path: str) -> Path:
    """Validate that config path points to an existing file."""
    path = Path(file_path)
    if not path.is_file():
        raise argparse.ArgumentTypeError(
            f"Config file does not exist: {file_path}",
        )
    return path


def build_parser() -> argparse.ArgumentParser:
    """Create CLI parser for the log analyzer."""
    parser = argparse.ArgumentParser(description=PROJECT_DESCRIPTION)
    parser.add_argument(
        "-c",
        "--config",
        type=existing_file,
        help="Path to config file.",
    )
    return parser


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""
    return build_parser().parse_args(args)


def _run_with_config(args: list[str] | None = None) -> None:
    parsed_args = parse_args(args)
    parsed_config = parse_config(parsed_args.config)
    logger = configure_logger(parsed_config.get("LOG_FILE"))
    logger.info(
        "config_loaded",
        config_path=str(parsed_args.config) if parsed_args.config else None,
    )
    analyze(parsed_config, logger)


def main(args: list[str] | None = None) -> int:
    """CLI entry point."""
    logger = configure_logger()
    try:
        _run_with_config(args)
    except KeyboardInterrupt:
        logger.error("unexpected_error", exc_info=True)
        return 1
    except Exception:
        logger.error("unexpected_error", exc_info=True)
        return 1

    return 0
