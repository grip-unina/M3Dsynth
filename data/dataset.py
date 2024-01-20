import os
import numpy as np
import random
import pandas
from utils.tiff_utils import load_slice_tiff_scan, get_shape_tiff_scan
from utils.tiff_utils import get_percentile_tiff_scan, apply_percentile
from torch.utils.data.dataset import Dataset
from torch import from_numpy as numpy2torch


def get_table_date(name_set, mods):
    tab = pandas.read_csv('./data/data.csv')
    tab = tab.merge(pandas.read_csv('./data/sets.csv'))
    tab = tab.merge(pandas.read_csv('./data/centers.csv'))
    tab = tab[tab['set']==name_set]
    tab = tab[tab['mod'].isin(mods)]
    return tab


def get_random_slide(in_dim, pos, out_dim, r):
    """
    Random crop the 512x512xz scans around the nodule's coord. It is necessary to avoid OOM issue.
    """
    pad = max(out_dim - in_dim, 0)
    total_start = (pad // 2) - pad
    total_end = in_dim + pad // 2
    
    start = min(max(pos - r - out_dim // 2, total_start), total_end - out_dim)
    end   = min(max(pos + r - out_dim // 2, total_start), total_end - out_dim)
    left = random.randint(start, end)
    return (left, left + out_dim)


def crop_and_padding(x, axis, start, end):
    dim = x.shape[axis]
    slc = [slice(None),] * x.ndim
    slc[axis] = slice(max(start, 0), min(end, dim))
    x = x[tuple(slc)]
    
    if (start<0) or (end>dim):
        npad = [(0, 0),] * x.ndim
        npad[axis] = (max(-start, 0), max(end-dim, 0))
        x = np.pad(x, pad_width=npad, mode='constant', constant_values=0)
        
    return x


def absdiff(a,b):
    return np.maximum(a,b) - np.minimum(a,b)


class M3Dsynth(Dataset):
    def __init__(self, M3Dsynth_dir, tab, output_shape, random_crop=True, aug_fun=None):
        self.tab = tab.copy()
        self.path_scan = f'{M3Dsynth_dir}/%s/scan/%s'
        self.path_label = f'{M3Dsynth_dir}/%s/label/%s'
        self.aug_fun = aug_fun
        
        if isinstance(output_shape, list) or isinstance(output_shape, tuple):
            self.output_shape = tuple(output_shape)
        else:
            self.output_shape = (int(output_shape), int(output_shape), int(output_shape))
        
        if random_crop:
            self.rdim = tuple([4 + max((_-40)//2,0) for _ in self.output_shape])
        else:
            self.rdim = None
            if self.output_shape[0]==1:
                self.tab['center_test_z'] = self.tab['coord_z']
            
            if 2*np.max(np.absdiff(self.tab['coord_z'], self.tab['center_test_z'])) > self.output_shape[0]:
                self.tab['center_test_z'] = self.tab['coord_z']
            
            if 2*np.max(np.absdiff(self.tab['coord_y'], self.tab['center_test_y'])) > self.output_shape[1]:
                self.tab['center_test_y'] = self.tab['coord_y']
            
            if 2*np.max(np.absdiff(self.tab['coord_x'], self.tab['center_test_x'])) > self.output_shape[2]:
                self.tab['center_test_x'] = self.tab['coord_x']
        
    def __len__(self):
        return len(self.tab)
    
    def __getitem__(self, idx):
        _data = self.tab.iloc[idx]
        dirname = self.path_scan % (_data['mod'], _data['img_id'])
        coord = (_data['coord_z'], _data['coord_y'], _data['coord_x'])
        
        ct_scan_shape = get_shape_tiff_scan(dirname)
        ct_scan_perc = get_percentile_tiff_scan(dirname, np.uint16)
        if self.rdim is None:
            centers = (int(_data['center_test_z']), int(_data['center_test_y']), int(_data['center_test_x']))
            z_crop, y_crop, x_crop = [(c-(od//2),  c+od-(od//2))
                                      for c, od in zip(centers, self.output_shape)]
        else:
            z_crop, y_crop, x_crop = [get_random_slide(int(dim), int(c), int(od), int(r))
                                      for dim, c, od, r in zip(ct_scan_shape, coord, self.output_shape, self.rdim)]
        ct_scan = load_slice_tiff_scan(dirname, ct_scan_shape, np.uint16, *z_crop)
        ct_scan = crop_and_padding(ct_scan, 1, *y_crop)
        ct_scan = crop_and_padding(ct_scan, 2, *x_crop)
        assert ct_scan.shape==self.output_shape
        
        if _data['mod'] in ('real',):
            ct_label = np.zeros(ct_scan.shape, dtype=np.bool_)
        else:
            ct_label = load_slice_tiff_scan(self.path_label % (_data['mod'], _data['img_id']),
                                       ct_scan_shape, np.bool_, *z_crop)
            ct_label = crop_and_padding(ct_label, 1, *y_crop)
            ct_label = crop_and_padding(ct_label, 2, *x_crop)
            assert ct_label.shape==self.output_shape
        
        ct_scan = apply_percentile(np.float32(ct_scan), *ct_scan_perc)[None, ...]
        ct_label = np.float32(ct_label)[None, ...]
        ct_scan  = numpy2torch(ct_scan)
        ct_label = numpy2torch(ct_label)

        if self.aug_fun is not None:
            dat = self.aug_fun({'image': ct_scan, 'mask': ct_label})
            ct_scan = dat['image']
            ct_label = dat['mask']
        
        return dict(image=ct_scan,
                    label=ct_label,
                    orig_id=_data['orig_id'],
                    img_id=_data['img_id'],
                    mod=_data['mod'],
                    coord=coord)
