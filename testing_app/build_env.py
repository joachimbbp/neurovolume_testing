from pathlib import Path


def root():
    return Path(__file__).parent.parent


def build():
    data = {"ROOT": root(), "HAM": "spam"}
    env_path = root() / "./.env"
    with open(env_path, "w") as f:
        for key, value in data.items():
            f.write(f"{key}={value}\n")


build()
