import geo
import mri
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
# ct.bunny()

# geo.pyramid()

anat = mri.anat()
print("anat: ", str(anat))

bold = mri.bold()
print("bold: ", str(bold))


# test_mri.bold(vdb_out, bold)
# render.render_tests()
