import os

#warn: must load_dotenv first!
def env_field(name: str):
    return str(os.getenv(name))
