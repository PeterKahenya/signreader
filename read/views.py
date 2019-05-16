import os
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import base64
import numpy as np
from .context import get_classes
from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import codecs

#commonly used variables and paths
WORK_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR=os.path.join(WORK_DIR,"models")

TRAIN_DIR=os.path.join(os.path.join(WORK_DIR,"images"),"train")
PREDICT_DIR=os.path.join(os.path.join(WORK_DIR,"images"),"predict")
IMAGE_DIM=224

#on-time setups
if not os.path.exists(PREDICT_DIR):
    os.makedirs(PREDICT_DIR)
    os.makedirs(os.path.join(PREDICT_DIR,"a"))
UPLOADED_FILE_URL = os.path.join(os.path.join(PREDICT_DIR,"a"),"photo.jpg")
CLASSES,CLASSES_COUNT=get_classes(TRAIN_DIR)
MODEL=None
if os.path.exists(os.path.join(MODEL_DIR,"model.hd5")):
	MODEL=load_model(os.path.join(MODEL_DIR,"model.hd5"))
	print("model loaded...")
else:
    MODEL=None

def detect_sign():
    prob=0.0
    sign=""
    if MODEL:
        predict_batch=ImageDataGenerator(rescale=1./255).flow_from_directory(PREDICT_DIR,target_size=(IMAGE_DIM,IMAGE_DIM),classes=CLASSES,batch_size=1)
        train_batch=ImageDataGenerator(rescale=1./255).flow_from_directory(TRAIN_DIR,target_size=(IMAGE_DIM,IMAGE_DIM),classes=CLASSES,batch_size=10)

        predictions_array=MODEL.predict_generator(predict_batch,steps=1,verbose=0)
        prob=max(predictions_array[0])
        predicted_class_indices=np.argmax(predictions_array,axis=1)
        labels = (train_batch.class_indices)
        labels = dict((v,k) for k,v in labels.items())
        prediction = [labels[k] for k in predicted_class_indices]
        sign=prediction[0]
    else:
        sign="-1"
    print(sign,prob)
    return sign,prob



@csrf_exempt
def index(request):
    if request.method=="GET":
        return render(request,"read.html",None,None)
    else:
        if request.method=="POST":
            #decode image data
            hand_roi=request.POST['hand_roi']
            hand_roi=hand_roi.replace("data:image/png;base64,","")

            """ pad = len(hand_roi)%4
            hand_roi += "="*(4-pad)
            print(len(hand_roi)%4) """
            
            img_data=base64.b64decode(hand_roi)
            
            #save image
            img_file = open(UPLOADED_FILE_URL, "wb+")
            img_file.write(img_data)
            img_file.close()
            
            #resize to desired size for the model
            img=cv2.imread(UPLOADED_FILE_URL)
            img_resized=cv2.resize(img,(IMAGE_DIM,IMAGE_DIM))
            orig_resized_gray=cv2.cvtColor(img_resized,cv2.COLOR_BGR2GRAY)
            cv2.imwrite(UPLOADED_FILE_URL,orig_resized_gray)

            #detect sign
            sign,prob=detect_sign()
            
            return HttpResponse(sign)

        else:
            return HttpResponse("Method Not allowed!!")
