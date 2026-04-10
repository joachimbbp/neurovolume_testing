REPO ?= "https://github.com/joachimbbp/neurovolume.git"

# USER SET NEUROVOLUME COMMIT GIT HASH HERE:
HASH ?= ""

run:
	rm -rf ./neurovolume
	git clone $(REPO) ./neurovolume
	cd ./neurovolume && git checkout $(HASH)
	cd ./neurovolume && uv sync && uv run python -m ziglang build
	uv sync
