import csv
import glob, os, shutil
from tqdm import tqdm

f = open("/Dataset/dataset_complete_160.csv", "a")

counter = 0
with open('train.age_detected_vgg.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in tqdm (csv_reader):
        img = row[0].replace("/", "_")
        age = int(round(float(row[1]), 0))
        path = "/Dataset/complete_dataset_resized_160/" + str(img)
        if os.path.exists(path):
            f.write(str(img) + "," + str (age) + "\n")
            counter += 1
            print (counter)
print (counter)

#parte del csv che contiene annotazioni relative alle immagini selezionate dal dataset UTK
counter = 0
line = ""
os.chdir("/Dataset/complete_dataset_resized_160/")
for file in glob.glob("*.jpg"):
    if not file.startswith("n"):
        counter += 1
        age = int(file.split("_")[0])
        img = "utk_"+ str(counter) + ".jpg"
        line = str(img) + "," + str(age) + "\n"
        os.rename(file, img)
        f.write(line)

f.close()
