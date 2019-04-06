#import statements
import os
import cv2
import keras
from .context import get_classes
from django.shortcuts import render,HttpResponse
from keras.applications.mobilenetv2 import MobileNetV2
from keras.layers import Dense, Input, Dropout,Conv2D,MaxPooling2D,Flatten
from keras.models import Model,Sequential


#commonly used paths
WORK_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRAIN_DIR=WORK_DIR+"/images/train/"
VALIDATE_DIR=WORK_DIR+"/images/validate/"
MODEL_DIR=WORK_DIR+"/models/"
IMAGE_DIM=112


def create_and_train_model(images_count,train_batches=10):
    batches_per_epoch=int(images_count/train_batches)
    #one-time setups for each training session
    CLASSES,CLASSES_COUNT=get_classes(TRAIN_DIR)
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
    print(batches_per_epoch)
    train_batch=keras.preprocessing.image.ImageDataGenerator(rescale=1./255).flow_from_directory(TRAIN_DIR,target_size=(IMAGE_DIM,IMAGE_DIM),classes=CLASSES,batch_size=train_batches)
    validate_batch=keras.preprocessing.image.ImageDataGenerator(rescale=1./255).flow_from_directory(VALIDATE_DIR,target_size=(IMAGE_DIM,IMAGE_DIM),classes=CLASSES,batch_size=2)

    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3),
                    activation='relu',
                    input_shape=(IMAGE_DIM,IMAGE_DIM,3)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(CLASSES_COUNT, activation='softmax'))
    
    #compile model using accuracy to measure model performance
    model.compile(optimizer=keras.optimizers.Adam(),loss='categorical_crossentropy',metrics=['accuracy'])
    #model.summary()
    #train model
    model.fit_generator(train_batch,steps_per_epoch=batches_per_epoch,validation_data=validate_batch,validation_steps=15,epochs=20,verbose=2)

    #save trained model
    model.save(MODEL_DIR+"model.hd5")

    return model

def index(request):
    total=0
    CLASSES,CLASSES_COUNT=get_classes(TRAIN_DIR)
    class_counts=[]
    for word in CLASSES:
        word_dict={}
        word_path=TRAIN_DIR+word
        count=len(os.listdir(word_path))
        total=total+count
        word_dict[word]=count
        class_counts.append(word_dict)
    if request.method=="GET":
        
        return render(request,"train.html",{'count':CLASSES_COUNT,"class_counts":class_counts,"total":total},None)
    else:
        if request.method=="POST":

            model=create_and_train_model(images_count=total,train_batches=15)

            return HttpResponse("model is trained")
        else:
            return HttpResponse("method not allowed")