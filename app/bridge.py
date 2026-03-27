# not sure what to call this
# basically builds a data structure
# that allows blender to read vdbs
# and attach the correct materials
# ...
# there's probably some industry
# jargon for this kind of thing but
# i went to film school so idk...

from pathlib import Path

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


def _vdb(vdb: Path) -> dict:
    """
    vdb with corresponding material name
    """
    return {
    "vdb": vdb.as_posix(),
    "mat": str(vdb.name),
    }

def build(vdbs_list: list[list[Path]]) -> dict:
    """
    returns nested dict
    bridge:
        entries (one for each image to be rendered):
            VDB info:
                contains vdb file and corresponding mat            
    """
    bridge = {}
    for vdbs in vdbs_list:
        entries = {}
        vdb_names = []
        for vdb in vdbs:
            name = str(vdb.stem)
            entries[name] = _vdb(vdb)
            vdb_names.append(name)
        bridge["-".join(vdb_names)] = entries
    return bridge
