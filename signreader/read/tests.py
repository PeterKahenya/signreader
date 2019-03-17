import os
import cv2
import base64
import keras
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import numpy as np
from keras.models import load_model
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator

from keras.models import Sequential,load_model
from keras.layers import Dense,Conv2D,Flatten


WORK_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PREDICT_DIR=WORK_DIR+"/images/predict/word/"
PREDICT_DIR_TEST=WORK_DIR+"/images/predict/"
MODEL_DIR=WORK_DIR+"/models/"
TRAIN_DIR=WORK_DIR+"/images/train/"



def newest(path):
        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files]
        return max(paths, key=os.path.getctime)

def get_all_words():
    words=[]
    for root, dirs, files in os.walk(TRAIN_DIR):
        for file in files:
            if file.endswith("jpg") or file.endswith("jpeg") or file.endswith("png"):
                path=os.path.join(root,file)
                word=os.path.basename(os.path.dirname(path))
                if not word in words:
                    words.append(word)
    
    return words,len(words)

def prepare_image():
    img = image.load_img(PREDICT_DIR+"photo.jpg", target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    return keras.applications.mobilenetv2.preprocess_input(img_array_expanded_dims)

def predict():
    words,size=get_all_words()
    train_batch=ImageDataGenerator(rescale=1./255).flow_from_directory(TRAIN_DIR,target_size=(224, 224),classes=words,color_mode="rgb",class_mode="categorical",batch_size=1)        
    predict_batch=ImageDataGenerator(rescale=1./255).flow_from_directory(PREDICT_DIR_TEST,target_size=(224, 224),classes=words,color_mode="rgb",class_mode="categorical",batch_size=1)            
    #processed_image=prepare_image()
    if model:
        predictions_array = model.predict_generator(predict_batch)
        predicted_class_indices=np.argmax(predictions_array,axis=1)
        labels = (train_batch.class_indices)
        labels = dict((v,k) for k,v in labels.items())
        prediction = [labels[k] for k in predicted_class_indices]
    else:
        prediction="No MODEL AVAILABLE"
    return prediction

if not os.path.exists(MODEL_DIR) or len(os.listdir(MODEL_DIR))==0:
    model=None
    print("No model available")
else:
    model_file=newest(MODEL_DIR)
    model=load_model(model_file)
    print("model loaded")


@csrf_exempt
def index(request):
    if request.method=="GET":
        return render(request,"read.html",None,None)
    else:
        if request.method=="POST":
            hand_roi=request.POST['hand_roi']
            hand_roi=hand_roi.replace("data:image/png;base64,","")
            img_data = base64.b64decode(hand_roi)

            if not os.path.exists(PREDICT_DIR):
                        os.makedirs(PREDICT_DIR)
            uploaded_file_url = PREDICT_DIR+"photo.jpg"
            img_file = open(uploaded_file_url, "wb+")
            img_file.write(img_data)
            img_file.close()
            
            img=cv2.imread(uploaded_file_url)
            img_resized=cv2.resize(img,(224,224))
            print(cv2.imwrite(uploaded_file_url,img_resized))

            word=predict()



            return HttpResponse("not ready")
        else:
            return HttpResponse("Method Not allowed!!")
            