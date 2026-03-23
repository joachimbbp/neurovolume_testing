import test_geo
import test_mri
import render
import env
import neurovolume as nv
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent.parent / ".env")
# NOTE: this has to be run form root
vdb_out = "./media/vdb_out"

env.build()

nv.hello()

test_geo.pyramid(vdb_out)
anat, bold = test_mri.download()

test_mri.anat(vdb_out, anat)
test_mri.bold(vdb_out, bold)
render.render_tests()
