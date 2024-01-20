import os
import pandas
import tqdm
from sys import argv
from utils.dicom_utils import load_dicom_scan, scan_to_uint16
from utils.tiff_utils import save_tiff_scan
from multiprocessing import get_context

path_lidc_idri = argv[1]
output_dir_path = argv[2]
numThreads = 8


tab_img = pandas.read_csv('./data/data.csv')
tab_img = tab_img[tab_img['mod']=='real'][['img_id','orig_id','sdir_id']]
tab_dicom = pandas.read_csv('./data/LIDC.csv')
tab_dicom = tab_dicom.merge(tab_img.groupby(['orig_id','sdir_id']).first().reset_index())
tab_dicom = tab_dicom.rename(columns={'img_id':'img_id_src'})
tab_img = tab_img.merge(tab_dicom)

def funpar(index):
    dicom_folder = os.path.join(path_lidc_idri, tab_dicom.loc[index,'dicom'])
    tiff_folder = os.path.join(output_dir_path, 'real/scan/', tab_dicom.loc[index,'img_id_src'])
    save_tiff_scan(tiff_folder, scan_to_uint16(load_dicom_scan(dicom_folder)))
    return 0

ctx  = get_context("fork")
with ctx.Pool(numThreads) as pool:
    list(tqdm.tqdm(pool.imap_unordered(funpar, tab_dicom.index), total=len(tab_dicom)))
    
for index in tqdm.tqdm(tab_img.index):
    src_folder = os.path.join(output_dir_path, 'real/scan/', tab_img.loc[index,'img_id_src'])
    dst_folder = os.path.join(output_dir_path, 'real/scan/', tab_img.loc[index,'img_id'])
    if src_folder!=dst_folder:
        os.symlink(src_folder, dst_folder, target_is_directory = True)
    