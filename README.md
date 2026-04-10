# Overview
Test suite for [neurovolume](neurovolume.com)

This app presently saves out two identitcal pyramid test patterns to `./media/output/vdb_out`:
one from a specific Neurovolume commit (set in the makefile) and the other using OpenVDB.
This is useful when benchmarking or trouble shooting the VDB writer. 

# usage:
## setup
Set your hash in the `Makefile`
**WARNING** this is, by default, blank!

```
# for example:
HASH ?= "28a4ee83a5a2de1d027d5797ae383e1294d53254"
```
blender and uv must be installed.

You can set up uv the usual way.

The Blender path *should* work. However, if it doesn't, that has been set up as an optional variable in `env.py`.

## to run:
from root:
`make run && uv run ./app/main.py`

`make run` to build the local neurovolume library.

`uv run ./app/main.py` to run the tests.

# Up Next
- [ ] add real world test to benchmark (see `main.wip`).
- [ ] Render out full “expected images” test suite using blender.
- [ ] Improve Pyramid test pattern and add custom pyramid material
