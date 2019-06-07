import cv2
import os

home = os.path.dirname(os.path.abspath(__file__))
for root, dirs, files in os.walk(os.path.join(home,'d')):
    for file in files:
        if file.endswith('.jpg'):
                path = os.path.join(root, file)
                img = cv2.imread(os.path.join(home, path))
                both_img = cv2.flip(img, +1)
                cv2.imwrite(path, both_img)
