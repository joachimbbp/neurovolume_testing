REPO ?= "https://github.com/joachimbbp/neurovolume.git"

# USER SET NEUROVOLUME COMMIT GIT HASH HERE:
HASH ?= "6db1dc0ad38d5738b4c3681e2769e86b5cb0c852"

run:
	rm -rf ./neurovolume
	git clone $(REPO) ./neurovolume
	cd ./neurovolume && git checkout $(HASH)
	cd ./neurovolume && uv sync && uv run python -m ziglang build
	uv sync
