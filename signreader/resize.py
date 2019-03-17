import os
import cv2
import datetime
TRAIN_DIR="images/validate/"
for root, dirs, files in os.walk(TRAIN_DIR):
                for file in files:
                    if file.endswith("jpg") or file.endswith("jpeg") or file.endswith("png"):
                        path=os.path.join(root,file)
                        orig=cv2.imread(path)
                        orig_resized=cv2.resize(orig,(28,28))
                        new_path=os.path.join(root,file)
                        cv2.imwrite(new_path,orig_resized)
            