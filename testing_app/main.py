import test_geo
import test_mri
import render
import datasets
import env
import neurovolume as nv
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(Path(__file__).parent.parent / ".env")
# NOTE: this has to be run form root
vdb_out = "./media/vdb_out"

env.build()

nv.hello()


# test_geo.pyramid(vdb_out)

test_mri.anat()
test_mri.bold()

# test_mri.bold(vdb_out, bold)
# render.render_tests()
