# not sure what to call this
# basically builds a data structure
# that allows blender to read vdbs
# and attach the correct materials
# ...
# there's probably some industry
# jargon for this kind of thing but
# i went to film school so idk...

from pathlib import Path

blender_files = Path(__file__).parent / "blender_files"
# then get the template file as a "renderer"
# set a "material holder" or s/t to the template as well

RENDERER = Path(__file__).parent / "./blendku"

def get_entry(vdb: Path, mat: str):
    entry = {
    "blender_file"
    "vdb": vdb.as_posix(),
    "mat": mat,
    }
