import sys
sys.path.append('C:\\Users\\egorp\\Desktop\\диплом\\файлы\\Python\\')

import numpy as np

from config import cfg


def enum(x):
    i = 0
    for item in x:
        if np.isnan(item):
            yield ('', np.nan)
        else:
            yield (i, item) 
            i += 1
    

def transpose(data: list[dict]) -> dict:
    outdict = {}

    for key in data[0].keys():
        outdict[key] = [d[key] for d in data]

    return outdict


def batches(lst: list, size: int):
    if size <= 0:
       return
    for i in range(0, len(lst), size):
        yield lst[i : i + size]


def create_connection_dict():
    conn_dict = {}
    with open(cfg.PATH_CLASSIFICATION, 'r') as data:
        for i, line in enumerate(data):
            if i == 0:
                continue
            line = line.split()
            conn_dict[(float(line[2]), int(line[3]))] = (int(line[0]), int(line[1]))
        
    return conn_dict

CONNECTION = create_connection_dict()


def find_by_elements(a: float, i: int):
    return CONNECTION.get((a, i))
    

def find_by_folder(folder: int, file: int):
    tmpConnection = dict(zip(CONNECTION.values(), CONNECTION.keys()))
    return tmpConnection.get((folder, file))