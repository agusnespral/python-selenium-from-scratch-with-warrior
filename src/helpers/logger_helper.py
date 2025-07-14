import logging
import os
from datetime import datetime


class LoggerHelper:
    _instance = None
    _logger_initialized = False  # Flag to track if configuration has run

    @staticmethod
    def get_instance():
        if LoggerHelper._instance is None:
            LoggerHelper()
        return LoggerHelper._instance

    def __init__(self):
        if LoggerHelper._instance is not None:
            # If an instance already exists, return it immediately without re-initializing
            return LoggerHelper._instance

        # This is the first initialization
        LoggerHelper._instance = self
        self._setup_logger()

    def _setup_logger(self):
        """Configures the logger, handlers, and formats."""

        # IMPORTANT: Do not use logging.basicConfig() here.
        # It only works once and can complicate logging in a test framework.
        # Instead, configure the logger manually.

        # 1. Get the main logger instance (you can name it, e.g., 'AutomationLogger')
        self.logger = logging.getLogger('AutomationLogger')

        # 2. Set the logger level to DEBUG to capture ALL messages
        self.logger.setLevel(logging.DEBUG)

        # Prevent adding handlers if they are already present (common issue in Pytest)
        if self.logger.handlers:
            return

        # 3. File Handler (for logging to a file)
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file = os.path.join(log_dir, f"test_log_{timestamp}.log")

        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        # Set File Handler to DEBUG so all messages are written to the file
        file_handler.setLevel(logging.DEBUG)

        # 4. Console Handler (for real-time output in the console)
        console_handler = logging.StreamHandler()
        # Set Console Handler to INFO to keep console output concise
        console_handler.setLevel(logging.INFO)

        # 5. Define Formatters
        file_formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s: %(message)s")
        console_formatter = logging.Formatter("%(levelname)s: %(message)s")

        file_handler.setFormatter(file_formatter)
        console_handler.setFormatter(console_formatter)

        # 6. Add Handlers to the Logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    # Public methods to use the logger
    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)

    def debug(self, message):
        # This will now be captured because the logger level is DEBUG
        self.logger.debug(message)