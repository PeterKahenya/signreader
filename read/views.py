import os
import cv2
import keras
import base64
import numpy as np
from .context import get_classes
from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt

#commonly used variables and paths
WORK_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR=WORK_DIR+"/models/"
TRAIN_DIR=WORK_DIR+"/images/train/"
PREDICT_DIR=WORK_DIR+"/images/predict/"
IMAGE_DIM=112

#on-time setups
if not os.path.exists(PREDICT_DIR):
    os.makedirs(PREDICT_DIR)
    os.makedirs(PREDICT_DIR+"a/")
UPLOADED_FILE_URL = PREDICT_DIR+"a/photo.jpg"
CLASSES,CLASSES_COUNT=get_classes(TRAIN_DIR)

if os.path.exists(MODEL_DIR+"model.hd5"):
    MODEL=keras.models.load_model(MODEL_DIR+"model.hd5")
    print("model loaded...")
else:
    MODEL=None



def detect_sign():
    sign=""
    if MODEL:
        predict_batch=keras.preprocessing.image.ImageDataGenerator(rescale=1./255).flow_from_directory(PREDICT_DIR,target_size=(IMAGE_DIM,IMAGE_DIM),classes=CLASSES,batch_size=1)
        train_batch=keras.preprocessing.image.ImageDataGenerator(rescale=1./255).flow_from_directory(TRAIN_DIR,target_size=(IMAGE_DIM,IMAGE_DIM),classes=CLASSES,batch_size=10)        
        predictions_array=MODEL.predict_generator(predict_batch,steps=1,verbose=0)    

        predicted_class_indices=np.argmax(predictions_array,axis=1)
        labels = (train_batch.class_indices)
        labels = dict((v,k) for k,v in labels.items())
        prediction = [labels[k] for k in predicted_class_indices]
        sign=prediction[0]
    else:
        sign="-1"
    print(sign)
    return sign    



@csrf_exempt
def index(request):
    if request.method=="GET":
        return render(request,"read.html",None,None)
    else:
        if request.method=="POST":

            #decode image data
            hand_roi=request.POST['hand_roi']
            hand_roi=hand_roi.replace("data:image/png;base64,","")
            img_data = base64.b64decode(hand_roi)

            #save imag
            img_file = open(UPLOADED_FILE_URL, "wb+")
            img_file.write(img_data)
            img_file.close()

            #resize to desired size for the model
            img=cv2.imread(UPLOADED_FILE_URL)
            img_resized=cv2.resize(img,(IMAGE_DIM,IMAGE_DIM))
            orig_resized_gray=cv2.cvtColor(img_resized,cv2.COLOR_BGR2GRAY)
            cv2.imwrite(UPLOADED_FILE_URL,orig_resized_gray)

            #detect sign
            sign=detect_sign()
            return HttpResponse(sign)
        else:
            return HttpResponse("Method Not allowed!!")