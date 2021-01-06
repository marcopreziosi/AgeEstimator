import argparse, os
import csv
import cv2

'''
Viene eseguito il crop delle immagini in base alle coordinate lette dal
file "annotation.csv"
'''


def init_parameter():
	parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('--images_path', help='Path to the folder where the image dataset is stored.', type=str)
	parser.add_argument('--padding', help='Padding for the crop', type=float, default=0.1)
	parser.add_argument('--output_path', help='Path where store the cropped images', type=str)
	return parser.parse_args()

args = init_parameter()

INPUT_SIZE = (224, 224)
counter=0
with open('annotation_vgg.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	for row in csv_reader:

		bbox = []
		image_path = args.images_path + row[2].replace('/', '_') 
		
		if os.path.exists(image_path):

		    frame = cv2.imread(image_path)
			x = int(row[4]) 
			y = int(row[5])
			w = int(row[6])
			h = int(row[7])
			
			bbox.append(x)
			bbox.append(y)
			bbox.append(x + w) 
			bbox.append(y + h)
			padding_px = 0
			face = frame[max(0,bbox[1]-padding_px):min(bbox[3]+padding_px,frame.shape[0]-1),max(0,bbox[0]-padding_px):min(bbox[2]+padding_px, frame.shape[1]-1)]
			resized_face = cv2.resize(face, INPUT_SIZE)
			cv2.imwrite(args.output_path+ row[2].replace('/', '_'), face)
			counter += 1
			print(counter)