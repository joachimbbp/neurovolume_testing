# TODO: from git hash
# for now we'll just do from local repos!
# 
NV_PATH ?= ../neurovolume
# run from the root with `make run`
run:
	rm -rf ./neurovolume
	cp -r $(NV_PATH)/. ./neurovolume
	rm -rf ./neurovolume/.venv
	cd ./neurovolume && uv sync && uv run python -m ziglang build
	uv sync
