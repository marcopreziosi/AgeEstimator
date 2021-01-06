from keras.models import load_model
import keras.backend as K
from keras.preprocessing import image
import numpy as np
import glob as glob
import argparse
import cv2 as cv2
import csv
from PIL import Image
from numpy import asarray

def init_param():
    parser = argparse.ArgumentParser()
    parser.add_argument("--view", type=int, default=0,  help="Show images")
    parser.add_argument("--dir", type=str,  help="Show images")
    parser.add_argument("--net", type=str,  help="Net path")
    parser.add_argument("--csv", type=str,  help="If it is not None, it writes on csv file")
    parser.add_argument("--crop", type=int, default=0,  help="if crop == 1, it reads annotation from --annotation csv file and it makes crop")
    parser.add_argument("--annotation", type=str,  help="Annotations for crop")
    parser.add_argument("--csv_input", type=str,  help="Csv of dataset to test")

    args = parser.parse_args()
    return args

#Accuracy che tiene conto del grado di confidenza della rete
def contrastive_accuracy(y_true, y_pred):
    return  1.0-K.mean(K.max(abs(y_pred-y_true),axis=1)) 

IMAGE_SIZE = (160, 160)

args = init_param()

if args.csv is not None:
    f = open(args.csv, 'w')


if args.crop:
    dict_annotation={}
    with open(args.annotation) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        key = ''
        for row in csv_reader:
            key = row[2].replace("/", "_", 1)
            x = int(row[4]) 
            y = int(row[5])
            w = int(row[6])
            h = int(row[7])
            dict_annotation[key] = (x,y,w,h)

#caricamento del modello
model = load_model(args.net, custom_objects= {'contrastive_accuracy': contrastive_accuracy})

err = 0
counter = 0
with open(args.csv_input) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        path = row[0]
        age = int(round(float(row[1]), 0))
        img = cv2.imread (str(args.dir) + str(path))
        #crop dell'immagine con le coordinate lette dall'annotation.csv
        if args.crop:
            bbox = []
            (x,y,w,h) = dict_annotation[row[0]]
            bbox.append(x)
            bbox.append(y)
            bbox.append(x + w) 
            bbox.append(y + h)
            padding_px = 0
            img = img[max(0,bbox[1]-padding_px):min(bbox[3]+padding_px,img.shape[0]-1),max(0,bbox[0]-padding_px):min(bbox[2]+padding_px, img.shape[1]-1)]
            img = cv2.resize(img, (160, 160))
        
        #Predict del modello
        img_p = np.reshape(img,[1,160,160,3])
        result = model.predict(img_p)
        img_class = np.argmax(result)
        err += abs(img_class-age)
        counter += 1
        #Stampa del MAE medio
        print (str(counter) + "\t\t" + str(err/counter))

        #Vuisualizzazione delle immagini
        if args.view:
            img=cv2.resize(img, (600, 600))
            cv2.putText(img, 'Age predicted: '+str(img_class) + "Age real: " + str(age), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            cv2.imshow('Age', img)
            if cv2.waitKey(0) == ord('q'):
                break

        if args.csv is not None:
            f.write(str(img)+', '+img_class+'\n')


print ("Il mae ottenuto è: " + str(err/counter))




