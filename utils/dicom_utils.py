import os
import numpy as np
import pydicom
#
# Utility functions to load and save scans in dicom format
#


def get_nslides_dicom_scan(dicom_folder):
    dcms = os.listdir(dicom_folder)
    dcms = [_ for _ in dcms if _.split('.')[-1] == 'dcm']
    return len(dcms)


def get_spacing_orientation_dicom_scan(dicom_folder):
    dcms = os.listdir(dicom_folder)
    dcms = [_ for _ in dcms if _.split('.')[-1] == 'dcm']
    fname = os.path.join(dicom_folder, dcms[0])
    with pydicom.dcmread(fname) as fid:
        spacing_xy  = fid.PixelSpacing
        spacing_z   = fid.SliceThickness
        spacing     = np.array([spacing_z, spacing_xy[1], spacing_xy[0]], dtype=np.float32) #zyx format
        orientation = np.transpose(fid.ImageOrientationPatient) #zyx format

    return spacing, orientation


def load_dicom_scan(dicom_folder):
    slices = list()
    indexes = list()
    
    for dcm in os.listdir(dicom_folder):
        if dcm.endswith('.dcm'):
            with pydicom.read_file(os.path.join(dicom_folder, dcm)) as slice_data:
                slices.append(slice_data.pixel_array)
                indexes.append(-1*float(slice_data.ImagePositionPatient[2]))
 
    scan = np.stack([x for _, x in sorted(zip(indexes, slices))], 0)
    
    return scan


def scan_to_uint16(scan):
    if scan.dtype==np.uint16:
        return scan
    assert scan.dtype==np.int16
    list_min = [0, 512, 1024, 2000, 2048]
    vmin = -np.min(scan)
    if vmin not in list_min:
        f = min(5, scan.shape[0])
        o = np.stack((scan[ :f, :5, :5],
                      scan[ :f, :5,-5:],
                      scan[ :f,-5:, :5],
                      scan[ :f,-5:,-5:],
                      scan[-f:, :5, :5],
                      scan[-f:, :5,-5:],
                      scan[-f:,-5:, :5],
                      scan[-f:,-5:,-5:],),0)
        vmin = -np.median(o)
        if vmin not in list_min:
            vmin = list_min[np.argmax([np.count_nonzero(o == -1*_) for _ in list_min])]
    
    assert vmin in list_min
    return np.uint16(scan.clip(min=-vmin) + vmin)