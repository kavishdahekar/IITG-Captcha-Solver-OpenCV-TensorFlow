# *******************************
# File 		: segregate.py
# Author 	: Kavish N. Dahekar
# Email 	: kavishdahekar@gmail.com
# Details 	: Script for processing annotated captchas, segmenting them into characters and placing them in seperate labeled folders
# *******************************

# this file mainly serves two purposes :
# 		1. Allow for quick checking whether all the data is correctly annotated. If we put all same characters in a single folder, it will be easy to check manually whether all of them are correct or not
# 		2. Segmenting the image in pre-processing makes training phase a bit faster

# this file will do the following
# 	read the captcha images
# 	segment the image into characters
# 	put the character images in character specific folder

import numpy as np
import cv2
import sys,os

# get files from collected annotated data
dataDir = "../data_collection/data"
# output directory
opDir = "segmented_data"

# read files
files = os.listdir(dataDir)

progress = 1

for file in files:
	if not file[:4] == "tmp_":
		# process filename
		filename = file.split('_')[1]
		chars = list(filename[:-4])
		
		# ------------------
		# segment the image

		# load image in grayscale
		img = cv2.imread(dataDir+"/"+file,1)
		print(dataDir+"/"+file)
		# convert to grayscale
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		# apply b&w threshold
		ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

		# medianBlur for removing salt and pepper noise
		median = cv2.medianBlur(thresh,3)
		# back to BGR so we have 3 channel colors for each pixel
		img = cv2.cvtColor(median,cv2.COLOR_GRAY2BGR)

		# erode and dilate
		kernel = np.ones((2,2),np.uint8)
		img = cv2.erode(img,kernel,iterations = 1)
		img = cv2.dilate(img,kernel,iterations = 1)

		# make copy
		charcpy = np.empty_like(img)
		np.copyto(charcpy,img)

		height, width, ch = img.shape

		# count total white pixels (required for clustering)
		colwise_wlist = []
		totalwhite = 0

		for col in range(width):
			wctr = 0
			bctr = 0
			for row in range(height):
				if np.array_equal(img[row][col] , np.array([255,255,255])):
					wctr += 1
					totalwhite += 1
			colwise_wlist.append(wctr)

		# prepare data for clustering
		a = np.zeros(shape=(totalwhite,2))
		ctr = 0
		for row in range(height):
			for col in range(width):
				if np.array_equal(img[row][col] , np.array([255,255,255])):
					a[ctr] = np.array([row,col])
					ctr += 1

		# applying kmeans on colwise white pixel counts
		z = np.float32(a)
		# Define criteria = ( type, max_iter = 10 , epsilon = 1.0 )
		criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
		# Set flags (Just to avoid line break in the code)
		flags = cv2.KMEANS_RANDOM_CENTERS
		K = 5
		# Apply KMeans
		compactness,labels,centers = cv2.kmeans(z,K,None,criteria,10,flags)

		# define colors to be used
		colors = [np.array([255,0,0]),np.array([0,255,0]),np.array([0,0,255]),np.array([255,255,0]),np.array([255,0,255])]
		imcpy = np.empty_like(img)
		np.copyto(imcpy,img)

		# draw colors according to cluster labels
		for i in range(len(a)):
			row,col = a[i][0],a[i][1]
			thisColor = colors[labels[i]]
			imcpy[row][col] = thisColor

		for c in range(len(centers)):
			Crow,Ccol = centers[c][0],int(centers[c][1])
			for row in range(height):
				imcpy[row][Ccol] = np.array([255,255,255])

		# characters
		charHeight, charWidth = height,45
		char_imgs = []
		centers = sorted(centers,key=lambda x: x[1])
		for c in range(len(centers)):
			Crow,Ccol = centers[c][0],int(centers[c][1])
			x1 = (Ccol-int(charWidth/2)) if ((Ccol-int(charWidth/2)) > 0) else 0
			x2 = (Ccol+int(charWidth/2)) if ((Ccol+int(charWidth/2)) < width) else width
			char_imgs.append(charcpy[0:height , x1:x2])

		for x in range(len(char_imgs)):
			opPath = opDir+"/"+ chars[x]
			if not os.path.exists(opPath):
				os.makedirs(opPath)
			cv2.imwrite(opPath +"/" + str(x) +"_" + file, char_imgs[x])


		# display progress
		print(str(progress)+"/"+str(len(files)))
		progress += 1
		