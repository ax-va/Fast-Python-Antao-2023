"""
Compare zipfile and fsspec on the inspection of zips contained csvs.

Motivation:
- zipfile -> re-opening zip for reading csv -> more mess
- fsspec -> less mess and no need to learn the zipfile interface
"""
import zipfile
import pandas as pd
from typing import Iterable
from fsspec.implementations.zip import ZipFileSystem


def describe_csvs_in_zips_with_zipfile(zip_files: Iterable[str]) -> None:
    """ Describe zips contained csvs with zipfile and Pandas """
    for zip_file in zip_files:
        print("zip_file:", zip_file)
        # Open the zip file using zipfile
        zf = zipfile.ZipFile(zip_file)
        for zf_info in zf.infolist():
            if not zf_info.filename.endswith(".csv"):
                continue
            print("\nzf_info.filename:", zf_info.filename)
            df = pd.read_csv(zipfile.Path(zf, zf_info.filename).open())
            print("df.describe():\n", df.describe())


def describe_csvs_in_zips_with_fsspec(zip_files: Iterable[str]) -> None:
    """ Describe zips contained csvs with fsspec and Pandas """
    for zip_file in zip_files:
        print("zip_file:", zip_file)
        zfs = ZipFileSystem(zip_file)
        # The find method, along with all others,
        # exists for all kinds of filesystems, not just for zip
        for filename in zfs.find(""):
            if not filename.endswith(".csv"):
                continue
            print("\nfilename:", filename)
            df = pd.read_csv(zfs.open(filename))
            print("df.describe():\n", df.describe())


describe_csvs_in_zips_with_zipfile(['dummy_copied.zip'])
# zip_file: dummy_copied.zip
#
# zf_info.filename: dummy1.csv
# df.describe():
#         col1  col2
# count   3.0   3.0
# mean    3.0   4.0
# std     2.0   2.0
# min     1.0   2.0
# 25%     2.0   3.0
# 50%     3.0   4.0
# 75%     4.0   5.0
# max     5.0   6.0
#
# zf_info.filename: dummy2.csv
# df.describe():
#          name     address
# count      3           3
# unique     3           3
# top     john  manchester
# freq       1           1

describe_csvs_in_zips_with_fsspec(['dummy_copied.zip'])
# zip_file: dummy_copied.zip
#
# filename: dummy1.csv
# df.describe():
#         col1  col2
# count   3.0   3.0
# mean    3.0   4.0
# std     2.0   2.0
# min     1.0   2.0
# 25%     2.0   3.0
# 50%     3.0   4.0
# 75%     4.0   5.0
# max     5.0   6.0
#
# filename: dummy2.csv
# df.describe():
#          name     address
# count      3           3
# unique     3           3
# top     john  manchester
# freq       1           1
