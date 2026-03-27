# not sure what to call this
# basically builds a data structure
# that allows blender to read vdbs
# and attach the correct materials
# ...
# there's probably some industry
# jargon for this kind of thing but
# i went to film school so idk...

from pathlib import Path

# hard coded config:
blender_files = Path(__file__).parent / "blender_files"
template_blend = blender_files / "template.blend"


def _entry(vdb: Path, mat: str):
    return {
    "blender_file": template_blend,
    "vdb": vdb.as_posix(),
    "mat": mat,
    }

def build(vdbs: list[Path]) -> dict:
    bridge = {}
    for vdb in vdbs:
        name = str(vdb.name)
        # WARN: this is sort of hack-y
        # and depends on a lot of hard-
        # coded paths being exactly right:
        # It assumes that the material
        # name is the same as the basename
        # of the vdb
        # ...
        # I don't love that pattern and
        # don't find it very maintainable
        # but seeing as I'm probably the
        # only person writing this test
        # suite for the time being it shouln't
        # be too much of a footgun. Of course
        # that's until I forget that this is
        # how I set it up, which is more or
        # less inevitable tbh
        bridge[name] = _entry(vdb, name)
    return bridge
