import numpy as np
import h5py
from PIL import Image 
import csv
import cv2

'''
Generazione del dataset in formato .h5py
Per quanto riguarda le label, queste sono state codificate in one-hot.
'''

label = []
images = []
counter = 0
label_one_hot = []
for i in range (101):
    label_one_hot.append(0)

with open('/Dataset/validation_160.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        age = int(round(float(row[1]), 0))
        label_one_hot = []
        for i in range (101):
            label_one_hot.append(0)

        for i in range (101):
            if i == age:
                label_one_hot[i] = 1
            else:
                label_one_hot[i] = 0
        label.append(label_one_hot)
        img = cv2.imread ("/Dataset/validation_160/"+ str(row[0]))
        images.append(img)
        counter += 1
        print(counter)


numpy_images_validation =  np.array(images)
numpy_label_validation = np.array(label)



label = []
images = []
counter = 0
with open('/Dataset/csv_for_tfrecord_3500_160.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        age = int(round(float(row[1]), 0))
        label_one_hot = []
        for i in range (101):
            label_one_hot.append(0)

        for i in range (101):
            if i == age:
                label_one_hot[i] = 1
            else:
                label_one_hot[i] = 0
        label.append(label_one_hot)
        img = cv2.imread ("/Dataset/training_160/"+ str(row[0]))
        images.append(img)
        counter += 1
        print(counter)


numpy_images_training =  np.array(images)
numpy_label_training = np.array(label)

print ("shape training")
print(numpy_images_training.shape)
print(numpy_label_training.shape)


print ("shape validation")
print(numpy_images_validation.shape)
print(numpy_label_validation.shape)


#Scrittura file 
f=h5py.File('dataset_complete_160.h5', 'w')
f.create_dataset('training', data=numpy_images_training)
f.create_dataset('validation', data=numpy_images_validation)
f.create_dataset('label_training', data=numpy_label_training)
f.create_dataset('label_validation', data=numpy_label_validation)
f.close()

