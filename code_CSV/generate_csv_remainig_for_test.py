import  csv, glob, os
import random
from datetime import datetime
import shutil

'''
File che serve per la generazione del csv di test che abbiamo adottato
per testare la rete. 
In particolare, abbiamo preso tutte le immagini che non abbiamo usato per il 
train e per il validation. 
'''

f = open("/Dataset/test_2000_160.csv", "a")

counter = 0
with open('train.age_detected_vgg.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        img = row[0].replace("/", "_")
        age = int(round(float(row[1]), 0))
        path = "Dataset/complete_data_2000_resized_160/" + str(img)
        if not os.path.exists(path):
            f.write(str(img) + "," + str (age) + "\n")
            counter += 1
            print (counter)
print ("Numero di samples disponibili per il test: " + str(counter))
