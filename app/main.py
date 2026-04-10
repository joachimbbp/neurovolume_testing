import env
from dotenv import load_dotenv
from pathlib import Path
import subprocess
import geo
from util import env_field as e
# RUN FROM ROOT!

env.build()
load_dotenv(Path(__file__).parent.parent / ".env")

# build the pyramid with Neurovolume
compare_folder = Path(e("vdb_out"))
geo.pyramid("neurovolume_pyramid")

# builds the pyramid with OpenVDB
subprocess.run(
    [
        "blender",
        "--background",  # no UI
        "--python",
        "./blender_scripts/openVDB_builder.py",
    ]
)

print("OpenVDB and Neurovolume written for comparison!")
