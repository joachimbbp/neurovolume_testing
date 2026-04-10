Test suite for [neurovolume](neurovolume.com)
# usage:
## setup
blender and uv must be installed.

You can set up uv the usual way.

The Blender path *should* work. However, if it doesn't, that has been set up as an optional variable in `env.py`.



## to run:
from root:
`make run && uv run ./app/main.py`

`make run` to build the local neurovolume library.

`uv run ./app/main.py` to run the tests.

# Up Next
- [ ] add BOLD to blender render.
- [ ] Render out full “expected images” test suite.
- [ ] Improve Pyramid test pattern and add custom pyramid material
