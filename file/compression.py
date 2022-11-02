import zipfile
from django.conf import settings


def compress_file(filename):
    with zipfile.ZipFile(filename, 'w') as zf:
        zf.write(filename, compress_type=zipfile.ZIP_DEFLATED)
    zf.close()
    zf.printdir()
    # print(zf)

def decompress_file(filename, original_name):
    with zipfile.Zipfile(filename, 'r') as zf:
        zf.extract(original_name)
    zf.close()
    # return zf