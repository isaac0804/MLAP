import csv
import os


def read_path(path):
    ret = []
    for (_, _, filenames) in os.walk(path):
        for file in filenames:
            ret.append(file)
    ret.sort()

    return ret
