import env
from dotenv import load_dotenv
from pathlib import Path
import subprocess

# RUN FROM ROOT!

env.build()
load_dotenv(Path(__file__).parent.parent / ".env")


subprocess.run(
    [
        "blender",
        "--background",  # no UI
        "--python",
        "./blender_scripts/openVDB_builder.py",
        # "./testing_app/blender_script.py",  # because you will run from root
    ]
)
