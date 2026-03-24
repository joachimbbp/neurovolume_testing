import os
import gzip
import shutil
from urllib.request import urlretrieve
import sys
import tarfile

def get_tar_gz(tar_gz_path: str, url:str):
    td = os.getenv('test_file_folder')    
    if (tar_gz_path or url) ==  "None":
            # HACK: the path stuff here is still hacky
            sys.exit(f"Error None value given as arg\ngz_path {tar_gz_path}\nurl: {url}")

    foldername = f"{tar_gz_path}".split("/")[-1][:-7]
    if not os.path.exists(tar_gz_path):
        print(f"Downloading {foldername} source file from {url}...")
        urlretrieve(url, tar_gz_path)
    else:
        print(f"{foldername} alreay exists")
    # TODO: some edge cases
    print("dir: ", dir)

    print(f"Unzipping to {dir}...")
    tar = tarfile.open(tar_gz_path, "r:gz")
    tar.extractall(path=str(td))
    tar.close()
    final_path = f'{td}/bunny_ct'
    os.rename(f'{td}/bunny',final_path)
    return final_path
    
def get_gz(gz_path: str, url: str):
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
        print(f"Unzipping to {filepath}...")
        with gzip.open(gz_path, "rb") as f_in:
            with open(filepath, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
    return filepath

