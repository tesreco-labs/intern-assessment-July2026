import logging
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOG_FILE = PROJECT_ROOT / "tesreco.log"


def get_logger(name="tesreco"):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def log_login_event(username):
    get_logger().info("Login event: %s logged in", username)


def log_error(message):
    get_logger().error("Error: %s", message)


def log_report_generation(report_name):
    get_logger().info("Report generation activity: %s generated", report_name)
