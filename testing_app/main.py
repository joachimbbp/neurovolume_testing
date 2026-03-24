import test_geo
import test_mri
import ct
import render
import datasets
import env
import neurovolume as nv
from dotenv import load_dotenv
from pathlib import Path


env.build()

load_dotenv(Path(__file__).parent.parent / ".env")

nv.hello()
ct.bunny()

# test_geo.pyramid(vdb_out)

# test_mri.anat()
# test_mri.bold()

# test_mri.bold(vdb_out, bold)
# render.render_tests()
