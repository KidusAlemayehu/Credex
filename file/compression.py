import zipfile
import pathlib
import os

def compress_file(path):
    file_path = path
    filename = open(path, 'r')
    fpath = pathlib.Path(file_path)
    zf_path = "".join([fpath.stem,".zip"])
    zf_path=os.path.join(fpath.parent,zf_path)
    print(zf_path)
    with zipfile.ZipFile(zf_path, mode='w') as zf:
        dir, base_filename = os.path.split(path)
        os.chdir(dir)
        zf.write(base_filename, compress_type=zipfile.ZIP_BZIP2)
    # print(zf.getinfo)
    zf.close()
    zf.printdir()
    if os.path.exists(path):
        os.remove(path)
    else:
        print("Can not delete the file as it doesn't exists")
    print("___________________")
    print(zf.filename)
    print("___________________")

def decompress_file(filename, original_name):
    file_path = filename
    fpath = pathlib.Path(file_path)
    zf_path = "".join([fpath.stem,".zip"])
    zf_path=os.path.join(fpath.parent,zf_path)
    with zipfile.ZipFile(zf_path, 'r') as zf:
        dir, base_filename = os.path.split(filename)
        os.chdir(dir)
        zf.extract(original_name)
    zf.close()
    zf.printdir()
    if os.path.exists(zf_path):
        os.remove(zf_path)
    else:
        print("Can not delete the file as it doesn't exists")
    print("___________________")
    print(zf.filename)
    print("___________________")

