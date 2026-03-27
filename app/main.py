import geo
import mri
import ct
import render
import datasets
import bridge
import env
import neurovolume as nv
from dotenv import load_dotenv
from pathlib import Path

env.build()

load_dotenv(Path(__file__).parent.parent / ".env")

nv.hello()
ct_bunny = [ct.bunny()]

pyramid =  [geo.pyramid()]

fmri_overlay = [mri.t1(), mri.bold()]

bridge = bridge.build([pyramid, fmri_overlay, ct_bunny])


print(bridge)
# test_mri.bold(vdb_out, bold)
# render.render_tests()
