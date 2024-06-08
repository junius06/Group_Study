import torch
from glob import glob
import shutil
import os

img_path = '/Users/jhkim/learning/Github/Group_Study/Python/PROJECT40/origin_images/'

#img_list = glob(img_path + '/*.png', recursive=True)
#img_list.extend(glob(img_path + '/*.png'))

img_list = []
for i in os.listdir(img_path):
    img_list.append(img_path + i)

print(img_list)

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

img_move_path = r'./classify_poeple'

for img_path in img_list:
    results = model(img_path)
    print(img_path)
    results.save(r'./check_images')
    for pred in results.pred[0]:
        tag = results.names[int(pred[-1])]
        print(tag)
        
        if tag == "person":
            print("move")
            shutil.move(img_path, img_move_path + '\\' + os.path.basename(img_path))
            break