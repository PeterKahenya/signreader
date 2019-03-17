from django.test import TestCase

# Create your tests here.
import os
import datetime
from django.shortcuts import render,HttpResponse
import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import to_categorical
from keras.models import Sequential,load_model
from keras.layers import Dense, Input, Dropout,Conv2D,Flatten
from keras.applications.mobilenetv2 import MobileNetV2
from keras.utils import plot_model
from keras.models import Model
from keras.optimizers import Adam

WORK_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRAIN_DIR=WORK_DIR+"/images/train/"
VALIDATE_DIR=WORK_DIR+"/images/validate/"
MODEL_DIR=WORK_DIR+"/models/"
target_size=224

def get_all_words(directory):
    words=[]
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith("jpg") or file.endswith("jpeg") or file.endswith("png"):
                path=os.path.join(root,file)
                word=os.path.basename(os.path.dirname(path))
                if not word in words:
                    words.append(word)
    return words,len(words)

def newest(path):
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    return max(paths, key=os.path.getctime)




def create_model(no_of_words):
    model=Sequential()
    return model


def prepare_for_training():
    errors_and_warnings=""
    train_words,train_size=get_all_words(TRAIN_DIR)
    validate_words,validate_size=get_all_words(VALIDATE_DIR)

    if train_size!=validate_size:
        errors_and_warnings+="all labels should be represented in both the train and validate set"
    print("train test sizes verified")
    if not os.path.exists(MODEL_DIR):
            os.makedirs(MODEL_DIR)
    print("Model directory verified")

    if not len(os.listdir(MODEL_DIR))==0:
        print("model detected, reusing...")
        latest_model_file=newest(MODEL_DIR)
        print(latest_model_file)
        model=load_model(latest_model_file)
        errors_and_warnings+="\n Loading an existing model"
        print("old model loaded...")
    else:
        print("no model detected, creating new one")
        model=create_model(no_of_words=train_size)
        print("MODEL CREATED!!")

    return model,train_words,validate_words,validate_size,errors_and_warnings


def index(request):
    response=""
    if request.method=="GET":
        return render(request,"train.html",None,None)
    else:
        if request.method=="POST":
            model,train_words,validate_words,validate_size,errors_and_warnings=prepare_for_training()
            train_batch=ImageDataGenerator(rescale=1./255).flow_from_directory(TRAIN_DIR,target_size=(224, 224),classes=train_words,color_mode="rgb",class_mode="categorical",batch_size=1)
            validation_batch=ImageDataGenerator(rescale=1./255).flow_from_directory(VALIDATE_DIR,target_size=(224, 224),classes=validate_words,color_mode="rgb",class_mode="categorical",batch_size=1)        

            model.compile(optimizer=Adam(lr=0.001),loss="categorical_crossentropy",metrics=['accuracy'])

            model.fit_generator(
                            train_batch, 
                            steps_per_epoch=4,
                            validation_data=validation_batch,
                            validation_steps=4, 
                            epochs=20,
                            verbose=1
                                            )
        
            model.save(MODEL_DIR+"model.hd5")


            response+=errors_and_warnings
            return HttpResponse(response)
        else:
            return HttpResponse("Method Not allowed!!")
            