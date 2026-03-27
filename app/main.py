import json
import geo
import mri
import ct
# import render
import bridge
import env
import neurovolume as nv
from dotenv import load_dotenv
from pathlib import Path
from util import env_field as e

env.build()

load_dotenv(Path(__file__).parent.parent / ".env")

nv.hello()
ct_bunny = [ct.bunny()]

pyramid =  [geo.pyramid()]

fmri_overlay = [mri.t1(), mri.bold()]

b = bridge.build([pyramid, fmri_overlay, ct_bunny])

# print(bridge)
# render.from_bridge(b)
with open(e('bridge'), 'w') as f:
    json.dump(b, f, indent=4)    
for scene in b:
    with open(e('scene'), 'w') as f:
        f.write(scene)
