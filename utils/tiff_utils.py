import os
import numpy as np
from PIL import Image
#
# Utility functions to load and save scans in tiff format
#

def get_shape_tiff_scan(dirname):
    index = 0
    filename = dirname+'/slide%04d.tiff' % index
    with Image.open(filename) as img:
        W, H = img.size
    
    while os.path.isfile(filename):
        index = index + 1
        filename = dirname+'/slide%04d.tiff' % index
    
    return index, H, W

def load_tiff_scan(dirname, dtype):
    list_out = list()
    index = 0
    filename = dirname+'/slide%04d.tiff' % index
    while os.path.isfile(filename):
        with Image.open(filename) as img:
            list_out.append(np.asarray(img, dtype=dtype))
        index = index + 1
        filename = dirname+'/slide%04d.tiff' % index
    return np.stack(list_out, 0)

def load_slice_tiff_scan(dirname, shape, dtype, start, end):
    out = np.zeros((end-start,shape[1],shape[2]), dtype=dtype)
    
    for index in range(max(start,0), min(end, shape[0])):
        filename = dirname+'/slide%04d.tiff' % index
        with Image.open(filename) as img:
            out[index-start] = np.asarray(img, dtype=dtype)
    
    return out

def save_tiff_scan(dirname, scan, mode=None, compression='lzma'):
    # mode = 'I;16' for np.uint8
    # mode = '1' for np.bool_
    os.makedirs(dirname, exist_ok=True)
    for index in range(scan.shape[0]):        
        Image.fromarray(scan[index], mode=mode).save(dirname+'/slide%04d.tiff' % index, compression=compression, lossless=True)