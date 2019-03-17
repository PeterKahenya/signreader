#import statements
import os
import cv2
import keras
from .context import get_classes
from django.shortcuts import render,HttpResponse



#commonly used paths
WORK_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRAIN_DIR=WORK_DIR+"/images/train/"
VALIDATE_DIR=WORK_DIR+"/images/validate/"
MODEL_DIR=WORK_DIR+"/models/"
IMAGE_DIM=28



#one-time setups for each training session
CLASSES,CLASSES_COUNT=get_classes(TRAIN_DIR)
if not os.path.exists(MODEL_DIR):
            os.makedirs(MODEL_DIR)



def create_and_train_model():
    train_batch=keras.preprocessing.image.ImageDataGenerator().flow_from_directory(TRAIN_DIR,target_size=(IMAGE_DIM,IMAGE_DIM),classes=CLASSES,batch_size=2)
    validate_batch=keras.preprocessing.image.ImageDataGenerator().flow_from_directory(VALIDATE_DIR,target_size=(IMAGE_DIM,IMAGE_DIM),classes=CLASSES,batch_size=2)

    #initialize sequential model with 0 layers
    model=keras.models.Sequential()

    #add model layers
    model.add(keras.layers.Conv2D(64, kernel_size=3, activation="relu", input_shape=(3,IMAGE_DIM,IMAGE_DIM)))
    model.add(keras.layers.Conv2D(32, (3, 3), activation='relu'))
    model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(keras.layers.Dropout(0.25))
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(128, activation='relu'))
    model.add(keras.layers.Dropout(0.5))
    model.add(keras.layers.Dense(CLASSES_COUNT, activation="softmax"))

    #compile model using accuracy to measure model performance
    model.compile(optimizer=keras.optimizers.Adam(lr=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])

    #train model
    model.fit_generator(train_batch,steps_per_epoch=5,validation_data=validate_batch,validation_steps=2,epochs=1000,verbose=2)

    #save trained model
    model.save(MODEL_DIR+"model.hd5")

    return model


def index(request):
    if request.method=="GET":
        return render(request,"train.html",None,None)
    else:
        if request.method=="POST":
            # resize in the train path
            
            model=create_and_train_model()

            return HttpResponse("model is trained")
        else:
            return HttpResponse("method not allowed")