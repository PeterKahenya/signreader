#import statements
import os
import cv2
import tensorflow as tf
import tensorflow.keras as keras
from .context import get_classes
from django.shortcuts import render,HttpResponse
from tensorflow.keras.layers import Dense, Input, Dropout,Conv2D,MaxPooling2D,Flatten
from tensorflow.keras.models import Model,Sequential


#commonly used variables and paths
WORK_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR=os.path.join(WORK_DIR,"models")
TRAIN_DIR=os.path.join(os.path.join(WORK_DIR,"images"),"train")
VALIDATE_DIR=os.path.join(os.path.join(WORK_DIR,"images"),"validate")
IMAGE_DIM=400


def create_and_train_model(images_count,train_batches=10):
    batches_per_epoch=int(images_count/train_batches)
    #one-time setups for each training session
    CLASSES,CLASSES_COUNT=get_classes(TRAIN_DIR)
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
    print(batches_per_epoch)
    train_batch=tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255).flow_from_directory(TRAIN_DIR,target_size=(IMAGE_DIM,IMAGE_DIM),classes=CLASSES,batch_size=train_batches)
    validate_batch=tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255).flow_from_directory(VALIDATE_DIR,target_size=(IMAGE_DIM,IMAGE_DIM),classes=CLASSES,batch_size=2)

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
    model.compile(optimizer=tf.keras.optimizers.Adam(),loss='categorical_crossentropy',metrics=['accuracy'])
    #model.summary()
    #train model
    model.fit_generator(train_batch,steps_per_epoch=batches_per_epoch,validation_data=validate_batch,validation_steps=15,epochs=10,verbose=2)

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

            model=create_and_train_model(images_count=total,train_batches=2)

            return HttpResponse("model is trained")
        else:
            return HttpResponse("method not allowed")
