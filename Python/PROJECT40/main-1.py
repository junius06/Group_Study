import torch
from glob import glob

img_path = r'./origin_images'

img_list = glob(img_path + './*.png')
img_list.extend(glob(img_path + './*.png'))

print(img_list)