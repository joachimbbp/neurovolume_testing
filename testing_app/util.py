import os


def env_field(name: str):
    return str(os.getenv(name))
