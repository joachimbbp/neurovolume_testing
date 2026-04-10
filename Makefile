# run from the root with `make run`
REPO ?= "https://github.com/joachimbbp/neurovolume.git"
HASH ?= "961bef0cffce9c1bdb371c5939ac94b007b6332c"

run:
	rm -rf ./neurovolume
	git clone $(REPO) ./neurovolume
	cd ./neurovolume && git checkout $(HASH)
	cd ./neurovolume && uv sync && uv run python -m ziglang build
	uv sync
