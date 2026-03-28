# not sure what to call this
# basically builds a data structure
# that allows blender to read vdbs
# and attach the correct materials
# ...
# there's probably some industry
# jargon for this kind of thing but
# i went to film school so idk...

from pathlib import Path
import json
from util import env_field as e
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
    "mat": str(vdb.stem),
    }

def build(scenes_list: list[list[Path]]) -> dict:
    """
    scenes_list: list of lists. Each sub list
    contains all that will be rendered in a scene

    returns nested dict
    bridge:
        scenes:
            VDB info:
                contains vdb file and corresponding mat            
    """
    bridge = {}
    for vdbs in scenes_list:
        scenes = {}
        vdb_names = []
        for vdb in vdbs:
            name = str(vdb.stem)
            scenes[name] = _vdb(vdb)
            vdb_names.append(name)
        bridge["-".join(vdb_names)] = scenes
    # maybe a custom data structure would
    # make this more robust but idk
    with open(e('bridge'), 'w') as f:
        json.dump(bridge, f)
    return bridge
    # fools will tell you to OOP this!
    # perhaps they are correct...
    # but not TOO correct!
    # I mean a custom data structure
    # might help with consistency
    # and at that point it could
    # have methods

def debug(bridge: dict):
    print("bridge debugger running")
    for scene in bridge:
        print("scene: ", scene)
        for vdb in bridge[scene]:
            print("  vdb: ", vdb)
            print("    vdb path: ", bridge[scene][vdb]['vdb'])
            print("    vdb mat: ", bridge[scene][vdb]['mat'])
    
