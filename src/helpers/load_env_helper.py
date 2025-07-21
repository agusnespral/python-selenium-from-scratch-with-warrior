import os
import yaml
from dotenv import load_dotenv
from src.helpers.logger_helper import LoggerHelper


def set_env():
    config_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     "../config/config.yml")
    )
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
        env = config.get("env", "stg")

        env_file = os.path.abspath(
            os.path.join(os.path.dirname(__file__), f"../../.env.{env}"))

        load_dotenv(dotenv_path=env_file)

        logger = LoggerHelper.get_instance()
        env_capital = env.upper()

        logger.info(f"Environment: {env_capital}")


set_env()