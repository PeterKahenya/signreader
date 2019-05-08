#import statements
import os
import cv2
from django.shortcuts import render,HttpResponse
from tensorflow.keras.optimizers import SGD,Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout,Conv2D,MaxPooling2D,Flatten
from .context import get_classes

#commonly used variables and paths
WORK_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR=os.path.join(WORK_DIR,"models")
TRAIN_DIR=os.path.join(os.path.join(WORK_DIR,"images"),"train")
VALIDATE_DIR=os.path.join(os.path.join(WORK_DIR,"images"),"validate")
IMAGE_DIM=400


def create_and_train_model(images_count,train_batches=10):
    batches_per_epoch=int(images_count/train_batches)
    print(batches_per_epoch)
    #one-time setups for each training session
    CLASSES,CLASSES_COUNT=get_classes(TRAIN_DIR)
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
    train_batch=ImageDataGenerator(rescale=1./255).flow_from_directory(TRAIN_DIR,target_size=(IMAGE_DIM,IMAGE_DIM),classes=CLASSES,batch_size=1)
    validate_batch=ImageDataGenerator(rescale=1./255).flow_from_directory(VALIDATE_DIR,target_size=(IMAGE_DIM,IMAGE_DIM),classes=CLASSES,batch_size=1)

    model = Sequential()
    model.add(Conv2D(64, (3, 3), activation='relu',input_shape=(IMAGE_DIM,IMAGE_DIM,3)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(100, activation='relu'))
    model.add(Dense(CLASSES_COUNT, activation='softmax'))

    #compile model using accuracy to measure model performance
    model.compile(optimizer=Adam(),loss='categorical_crossentropy',metrics=['accuracy'])
    model.fit_generator(train_batch,steps_per_epoch=batches_per_epoch,validation_data=validate_batch,validation_steps=4,epochs=100,verbose=1)

    #save trained model
    model.save(os.path.join(MODEL_DIR,"model.hd5"))
    return model

def index(request):
    total=0
    CLASSES,CLASSES_COUNT=get_classes(TRAIN_DIR)
    class_counts=[]
    for word in CLASSES:
        word_dict={}
        word_path=os.path.join(TRAIN_DIR,word)
        count=len(os.listdir(word_path))
        total=total+count
        word_dict[word]=count
        class_counts.append(word_dict)
    if request.method=="GET":

        return render(request,"train.html",{'count':CLASSES_COUNT,"class_counts":class_counts,"total":total},None)
    else:
        if request.method=="POST":

            model=create_and_train_model(images_count=total,train_batches=1)

            return HttpResponse("model is trained")
        else:
            return HttpResponse("method not allowed")
