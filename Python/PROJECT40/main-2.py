import torch
from glob import glob

img_path = r'./origin_images'

img_list = glob(img_path + './*.png')
img_list.extend(glob(img_path + './*.png'))

print(img_list)

# yolov5 모델을 touch.hub에서 불러와서 사용한다.
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

for img_path in img_list:
    results = model(img_path)
    print(img_path)
    results.save(r'./image_check')
    for pred in results.pred[0]:
        tag = results.names[int(pred[-1])]
        print(tag)
        