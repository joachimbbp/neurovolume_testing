Test suite for [neurovolume](neurovolume.com)
# usage:
## setup
blender and uv must be installed.

You can set up uv the usual way.

This tests from your local neurovolume repository.
`env.build()` default assumes the neurovolume repo to live next to the neurovolume testing repo like so:

````shell
├── neurovolume
└── neurovolume_testing
````
However, that is just because it so happens to be that way on my machine. You can override this in `app/main.py`:
```python
env.build(source_repo="/path/to/your/neurovolume")
```
The Blender path *should* work. However, if it doesn't, that has likewise been set up as an optional variable.



## to run:
from root:
`make run && uv run ./app/main.py`

`make run` to build the local neurovolume library.

`uv run ./app/main.py` to run the tests.

# Up Next
- [ ] add BOLD to blender render.
- [ ] Render out full “expected images” test suite.
- [ ] Improve Pyramid test pattern and add custom pyramid material