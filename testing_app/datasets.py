import os
import gzip
import shutil
from urllib.request import urlretrieve
import sys

def get(gz_path: str, url: str):
    """download and unzips file"""
    if (gz_path or url) ==  "None":
        # HACK: the path stuff here is still hacky
        sys.exit(f"Error None value given as arg\ngz_path {gz_path}\nurl: {url}")

    filename = f"{gz_path}".split("/")[-1][:-3]
    filepath = f"{os.getenv('test_file_folder')}/{filename}"
    if not os.path.exists(gz_path):
        print(f"Downloading {filename} source file from {url}...")
        urlretrieve(url, gz_path)
    else:
        print(f"{filename} alreay exists")
    # TODO: some edge cases
    if not os.path.exists(filepath):
        print(f"Unzipping {filepath}")
        with gzip.open(gz_path, "rb") as f_in:
            with open(filepath, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
    return filepath

