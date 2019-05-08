import os
import numpy as np
import tensorflow.keras as keras
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

WORK_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR=os.path.join(os.path.join(WORK_DIR,"temp"),"models")
PREDICT_DIR=os.path.join(os.path.join(WORK_DIR,"images"),"predict")
IMAGE_DIM=224

MODEL=load_model(os.path.join(MODEL_DIR,"model.hd5"))
test_image = image.load_img(os.path.join(os.path.join(PREDICT_DIR,'a'),'photo.jpg'), target_size=(IMAGE_DIM, IMAGE_DIM))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis=0)

img=keras.applications.mobilenet.preprocess_input(test_image)

predictions=MODEL.predict(img)
print(predictions)
predictions=MODEL.predict(img)
print(predictions)
predictions=MODEL.predict(img)
print(predictions)