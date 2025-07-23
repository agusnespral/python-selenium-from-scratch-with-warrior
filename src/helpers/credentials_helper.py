from dotenv import load_dotenv
import os
from src.helpers.load_env_helper import set_env
from collections import namedtuple

set_env()

Credentials = namedtuple("Credentials", ["username", "password"])


def get_credentials(variant="valid"):
    if variant == "valid":
        user = os.getenv("QA_USERNAME")
        pwd = os.getenv("QA_PWD")
    elif variant == "invalid_username":
        user = os.getenv("QA_INVALID_USERNAME")
        pwd = os.getenv("QA_PWD")
    elif variant == "invalid_password":
        user = os.getenv("QA_USERNAME")
        pwd = os.getenv("QA_INVALID_PWD")

    else:
        raise ValueError(
            "QA_EMAIL and QA_PWD must be set in .env.stg")

    return Credentials(username=user, password=pwd)



