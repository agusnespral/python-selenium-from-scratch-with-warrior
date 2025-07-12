import os
from datetime import datetime

# from src.main.helpers.logger_helper import LoggerHelper


class ScreenshotHelper:
    def __init__(self, screenshot_dir="screenshots"):
        self.screenshot_dir = screenshot_dir
        os.makedirs(self.screenshot_dir, exist_ok=True)
        # self.logger = LoggerHelper.get_instance()

    def take_screenshot(self, driver, test_name: str, step: str = ""):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        step_part = f"_{step}" if step else ""
        filename = f"{test_name}{step_part}_{timestamp}.png"
        filepath = os.path.join(self.screenshot_dir, filename)

        driver.save_screenshot(filepath)
        # self.logger.info(f"📸 Screenshot saved to: {filepath}")
        return filepath
