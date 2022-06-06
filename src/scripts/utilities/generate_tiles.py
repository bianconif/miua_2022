"""Generate images showing snapshots of the lesions"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pylidc as pl
from pylidc.utils import consensus
from skimage.measure import find_contours
from sklearn import preprocessing

from functions.utilities import get_config

config = get_config()

scans_df = pd.read_csv(filepath_or_buffer = config['scans_metadata_file'])
nodules_df = pd.read_csv(filepath_or_buffer = config['nodules_metadata_file'])

[hu_min, hu_max] = config['window_limits_tiles'] 

#Read the nodules metadata
df_nodules = pd.read_csv(filepath_or_buffer = config['nodules_metadata_file'])

#Filter by number of annotations
df_nodules = df_nodules[df_nodules['num_annotations'] >= config['min_annotations_per_nodule']]

patient_ids = df_nodules['patient_id'].unique()
patient_ids.sort()

for patient_id in patient_ids:
    
    #Get the scan metadata and volume
    scan = pl.query(pl.Scan).filter(pl.Scan.patient_id == patient_id).first()
    pixel_spacing = scan.pixel_spacing
    vol = scan.to_volume()
    
    #Compute the image size based on the scale factor
    image_size = np.ceil(config['side_length_tiles']/pixel_spacing)   
    
    #Iterate the nodules
    nodules = scan.cluster_annotations()
    for i, nodule in enumerate(nodules):
        
        base_pad = 10
        
        cmask,cbbox,masks = consensus(nodule, clevel=0.5)
        
        #Pad to square
        v_pad = int(np.ceil((image_size - cmask.shape[0])/2))
        h_pad = int(np.ceil((image_size - cmask.shape[1])/2))
        pad = [(v_pad, v_pad), (h_pad, h_pad), (0,0)]  
        
        try:
            cmask,cbbox,masks = consensus(nodule, clevel=0.5, pad = pad)         
        
            #Get the central slice of the computed bounding box.
            k = int(0.5*(cbbox[2].stop - cbbox[2].start))   
            slice_ = vol[cbbox][:,:,k]
        
            #Resample the window signal between the given limits
            slice_[slice_ > hu_max] = hu_max
            slice_[slice_ < hu_min] = hu_min
            slice_ = (slice_ - hu_min)/(hu_max - hu_min)
        
            #Set up the plot.
            fig , ax = plt.subplots(1,1,figsize=(5,5))
            ax.imshow(slice_, cmap=plt.cm.gray, alpha=0.5)   
        
            #Plot the 50% consensus contour for the kth slice.
            for c in find_contours(cmask[:,:,k].astype(float), 0.5):
                plt.plot(c[:,1], c[:,0], '--k', linewidth = 2.0)   
            
            ax.axis('off')
            plt.tight_layout()
            plt.savefig(f'{config["tiles_folder"]}/{patient_id}--{i:03d}.png', bbox_inches="tight")
            plt.close('all')
        except:
            pass
