from setuptools import setup, Extension
import sys
import re
import os
import subprocess

_min_version = 3, 4
if sys.version_info < _min_version:
    raise Exception("Python %d.%d or later is required" % _min_version)

include_dirs = []
library_dirs = ['/usr/local/lib']

if sys.platform == 'linux2':
    os.environ['PATH'] += ":/usr/local/bin:$home/bin:.:..:../.."

    tcinc = subprocess.getoutput('tcucodec conf -i 2>/dev/null')
    minc = re.search(r'-I([/\w]+)', tcinc)
    if minc:
        for path in minc.groups():
            include_dirs.append(path)
        include_dirs = sorted(set(include_dirs), key=include_dirs.index)

    tclib = subprocess.getoutput('tcucodec conf -l 2>/dev/null')
    mlib = re.search(r'-L([/\w]+)', tclib)
    if mlib:
        for path in mlib.groups():
            library_dirs.append(path)
        library_dirs = sorted(set(library_dirs), key=library_dirs.index)

setup(
    name="tokyocabinet",
    version="0.6",
    packages=['tokyocabinet'],
    ext_modules=[
        Extension(
            "tokyocabinet.btree", ['tokyocabinet/btree.c'],
            libraries=["tokyocabinet"],
            include_dirs=include_dirs,
            library_dirs=library_dirs
        ),
        Extension(
            "tokyocabinet.hash", ['tokyocabinet/hash.c'],
            libraries=["tokyocabinet"],
            include_dirs=include_dirs,
            library_dirs=library_dirs
        ),
        Extension(
            "tokyocabinet.table", ['tokyocabinet/table.c'],
            libraries=["tokyocabinet"],
            include_dirs=include_dirs,
            library_dirs=library_dirs
        )
    ],
    description="""tokyocabinet aims to be a complete python wrapper for the 
        Tokyo Cabinet database library by Mikio Hirabayashi (http://1978th.net/).
        
        So far the btree, hash and table APIs have been fully wrapped.""",
    author="Elisha Cook",
    author_email="ecook@justastudio.com",
    url="https://github.com/leahfitch/python-tokyocabinet"
)
