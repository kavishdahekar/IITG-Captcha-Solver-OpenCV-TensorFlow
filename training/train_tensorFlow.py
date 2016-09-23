# *******************************
# File      : train_tensorFlow.py
# Author    : Kavish N. Dahekar
# Email     : kavishdahekar@gmail.com
# Details   : Defining, training and testing Neural Net using annotated data
# *******************************

import sys,os,pickle,random
import numpy as np
import tensorflow as tf

# training data previously stored as a dictionary and written to a pickle dump
training_data = pickle.load( open( "training_data.pickle", "rb" ) )
# character image width and height
imgheight, imgwidth = 65, 45

# charMap serves as a lookup table for determining what character is denoted by the index, example 0 is 2. and 27 is z.
charMap = ['2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','k','m','n','p','r','s','t','v','w','x','y','z']
# charMapR serves as a reverse lookup for determining the index of a character
charMapR = {}
charMapR['2'] = 0
charMapR['3'] = 1
charMapR['4'] = 2
charMapR['5'] = 3
charMapR['6'] = 4
charMapR['7'] = 5
charMapR['8'] = 6
charMapR['9'] = 7
charMapR['a'] = 8
charMapR['b'] = 9
charMapR['c'] = 10
charMapR['d'] = 11
charMapR['e'] = 12
charMapR['f'] = 13
charMapR['g'] = 14
charMapR['h'] = 15
charMapR['k'] = 16
charMapR['m'] = 17
charMapR['n'] = 18
charMapR['p'] = 19
charMapR['r'] = 20
charMapR['s'] = 21
charMapR['t'] = 22
charMapR['v'] = 23
charMapR['w'] = 24
charMapR['x'] = 25
charMapR['y'] = 26
charMapR['z'] = 27



# PREPARING DATA
inputData_x = [] # image, which is an input vector , 2925x1
inputData_y = [] # output, denoting the character from the image, 28x1

# add segmented data to well formatted list
for c in training_data:
    for i in range(len(training_data[c])):
        inputData_x.append(training_data[c][i][0])
        label_temp = [0]*28
        label_temp[charMapR[c]] = 1
        inputData_y.append(label_temp)

# add segmented data to well formatted list
inputData_x = np.array(inputData_x)
inputData_y = np.array(inputData_y)
print("total : ",len(inputData_x),len(inputData_y))

# shuffle the data
inputData = list(zip(inputData_x,inputData_y))
random.shuffle(inputData)
inputData_x,inputData_y = zip(*inputData)

# separate training and testing data
separateRatio = 0.20
testing_data_len = int(len(inputData_x) * separateRatio)
trainingData_x = inputData_x[:len(inputData_x)-testing_data_len]
trainingData_y = inputData_y[:len(inputData_y)-testing_data_len]

testingData_x = np.array(inputData_x[len(inputData_x)-testing_data_len:])
testingData_y = np.array(inputData_y[len(inputData_y)-testing_data_len:])

print("training : ",len(trainingData_x),len(trainingData_y))
print("testing  : ",len(testingData_x),len(testingData_y))


# **********************************************************************

# NEURAL NET
# ----------

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

# INIT NNet
# ---------

# training
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
# ready to run
init = tf.initialize_all_variables()
# Add ops to save and restore all the variables.
saver = tf.train.Saver()
# define session
sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
# run session (doesn't start training)
sess.run(init)

# TRAINING
# --------
# run training
for i in range(5000):
    # create batch of 100 random training samples
    batch_indices = random.sample(range(0, len(trainingData_x)), 100)
    batch_x = []
    batch_y = []
    for r in batch_indices:
        batch_x.append(trainingData_x[r])
        batch_y.append(trainingData_y[r])
    batch_x = np.array(batch_x)
    batch_y = np.array(batch_y)
    sess.run(train_step, feed_dict={x: batch_x, y_: batch_y})


# TESTING
# -------

# testing
correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
# accuracy
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))


print("Accuracy :",sess.run(accuracy, feed_dict={x: testingData_x, y_: testingData_y}))


# Save the variables to disk.
save_path = saver.save(sess, "trainedModels/softmaxNNModel.model")
print("Model saved to file: %s" % save_path)