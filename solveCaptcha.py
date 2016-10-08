# *******************************
# File      : solveCaptcha.py
# Author    : Kavish N. Dahekar
# Email     : kavishdahekar@gmail.com
# Details   : Using model for predicting captcha text
# *******************************

import sys,os,pickle,random
import numpy as np
import tensorflow as tf

import numpy as np
import cv2
import matplotlib

# Recreate neural network from model file generated during training
# input 
x = tf.placeholder(tf.float32, [None, 2925])
# weights
W = tf.Variable(tf.zeros([2925, 28]))
# biases
b = tf.Variable(tf.zeros([28]))

# model
y = tf.nn.softmax(tf.matmul(x, W) + b)
# correct_answers
y_ = tf.placeholder(tf.float32, [None, 28])

# error function
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

# Add ops to save and restore all the variables.
saver = tf.train.Saver()

# sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
sess = tf.Session()

# load model from file
saver.restore(sess, "training/trainedModels/softmaxNNModel.model")
print("Model restored from file : training/trainedModels/softmaxNNModel.model")


# --------------------------------------------------------------
# --------------------------------------------------------------
# --------------------------------------------------------------


# get image
# load image in grayscale
if len(sys.argv) != 2:
	print("\nPlease enter name of image to be processed as first argument.")
	print("\nExample usage :")
	print("\t\tpython solveCaptcha.py mycaptcha.png")
	sys.exit(-1)

img = cv2.imread(sys.argv[1],1)

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

charcpy = np.empty_like(img)
np.copyto(charcpy,img)

height, width, ch = img.shape
print(height,"x",width)

# count total white pixels
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

# extract the characters
charHeight, charWidth = height,45
char_imgs = []
centers = sorted(centers,key=lambda x: x[1])
for c in range(len(centers)):
	Crow,Ccol = centers[c][0],int(centers[c][1])
	x1 = (Ccol-int(charWidth/2)) if ((Ccol-int(charWidth/2)) > 0) else 0
	x2 = (Ccol+int(charWidth/2)) if ((Ccol+int(charWidth/2)) < width) else width

	temp_image = charcpy[0:height , x1:x2]
	
	
	# adjust the width
	for xx in range(len(temp_image[0]),45):
		temp_image = np.insert(temp_image, len(temp_image[0]), values=0, axis=1)

	temp_image = cv2.cvtColor(temp_image,cv2.COLOR_BGR2GRAY)
	tempret, tempthresh = cv2.threshold(temp_image,0,1,cv2.THRESH_BINARY)

	temp_image = np.reshape(tempthresh, (1, 2925))

	char_imgs.append(temp_image)




# -------------------------------------------------
# -------------------------------------------------
# -------------------------------------------------
charMap = ['2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','k','m','n','p','r','s','t','v','w','x','y','z']

# define the model
def model(x_in,Wts,bs):
	yop = tf.nn.softmax(tf.matmul(x_in, Wts) + b)
	return yop

# index of character
testi = 0

# final output
finOP = ""

# passing each of the 5 characters through the NNet
for testi in range(5):
	test_x = np.asarray(char_imgs[testi],dtype=np.float32)

	predict_op = model(test_x,W,b)

	op = sess.run(predict_op, feed_dict={x: test_x})

	# find max probability from the probability distribution returned by softmax
	max = op[0][0]
	maxi = -1
	for i in range(28):
	    if op[0][i] > max:
	        max = op[0][i]
	        maxi = i

	# append it to final output
	finOP += charMap[maxi]


print("\n\n\nOUTPUT :",finOP.upper())
print("\n\n\n")
