import numpy as np


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