#!/usr/bin/env python
# coding: utf-8

# # TASK #1: PROJECT OVERVIEW 
# 

# ![image.png](attachment:image.png)

# ![image.png](attachment:image.png)

# ![image.png](attachment:image.png)

# # TASK #2: IMPORT LIBRARIES/DATASETS

# In[2]:


import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import pandas as pd
import seaborn as sns
import pickle
import random


# ![image.png](attachment:image.png)

# In[3]:


with open("./traffic-signs-data/train.p", mode='rb') as training_data:
    train = pickle.load(training_data)
with open("./traffic-signs-data/valid.p", mode='rb') as validation_data:
    valid = pickle.load(validation_data)
with open("./traffic-signs-data/test.p", mode='rb') as testing_data:
    test = pickle.load(testing_data)


# In[4]:


X_train, y_train = train['features'],train['labels']
X_validation, y_validation = valid['features'],valid['labels']
X_test, y_test = test['features'],test['labels']


# In[5]:


# x_train.shape

print(X_train.shape)
print(X_validation.shape)
print(X_test.shape)


# In[6]:


y_train.shape


# # TASK #3: PERFORM IMAGES VISUALIZATION

# In[7]:


i = np.random.randint(1, len(X_train))
plt.imshow(X_train[i])
y_train[i]


# In[8]:


# Let's view more images in a grid format
# Define the dimensions of the plot grid 
W_grid = 10
L_grid = 10

# fig, axes = plt.subplots(L_grid, W_grid)
# subplot return the figure object and axes object
# we can use the axes object to plot specific figures at various locations

fig, axes = plt.subplots(L_grid, W_grid, figsize = (20,20))

axes = axes.ravel() # flaten the 5 x 5 matrix into 25 array

n_training = len(X_train) # get the length of the training dataset

# Select a random number from 0 to n_training
# create evenly spaces variables 
for i in np.arange(0, W_grid * L_grid):
    # Select a random number
    index = np.random.randint(0, n_training)
    # read and display an image with the selected index 
    axes[i].imshow(X_train[index])
    axes[i].set_title(y_train[index], fontsize = 18)
    axes[i].axis('off')
    
plt.subplots_adjust(hspace = 0.4)
    

        


# # TASK #4: CONVERT IMAGES TO GRAYSCALE AND PERFORM NORMALIZATION

# In[10]:


from sklearn.utils import shuffle
X_train, y_train = shuffle(X_train, y_train)
X_validation, y_validation = shuffle(X_validation, y_validation)
X_test, y_test = shuffle(X_test, y_test)


# In[12]:


X_train_gray = np.sum(X_train/3, axis = 3, keepdims = True)
X_test_gray = np.sum(X_test/3, axis = 3, keepdims = True)
X_validation_gray = np.sum(X_validation/3, axis = 3, keepdims = True)


# In[14]:


print(X_train_gray.shape)
print(X_test_gray.shape)
print(X_validation_gray.shape)


# In[18]:


X_train_gray_norm = (X_train_gray - 128)/128
X_validation_gray_norm = (X_validation_gray - 128)/128
X_test_gray_norm = (X_test_gray - 128)/128


# In[19]:


X_test_gray_norm


# In[ ]:





# In[32]:


i = random.randint(1, len(X_train_gray))
plt.imshow(X_train_gray[i].squeeze(), cmap = 'gray')
plt.figure()
plt.imshow(X_train[i])
plt.figure()
plt.imshow(X_train_gray_norm[i].squeeze(), cmap = 'gray')


# # TASK #5: UNDERSTAND THE THEORY AND INTUITION BEHIND CONVOLUTIONAL NEURAL NETWORKS 

# ![image.png](attachment:image.png)

# ![image.png](attachment:image.png)

# # TASK #6: BUILD DEEP CONVOLUTIONAL NEURAL NETWORK MODEL

# In[21]:


from tensorflow.keras import datasets, layers, models
CNN = models.Sequential()

CNN.add(layers.Conv2D(6, (5, 5), activation = 'relu', input_shape = (32, 32, 1)))
CNN.add(layers.AveragePooling2D())

CNN.add(layers.Dropout(0.2))

CNN.add(layers.Conv2D(16, (5, 5), activation = 'relu'))
CNN.add(layers.AveragePooling2D())

CNN.add(layers.Flatten())

CNN.add(layers.Dense(120, activation = 'relu'))
CNN.add(layers.Dense(84, activation = 'relu'))
CNN.add(layers.Dense(43, activation = 'softmax'))
CNN.summary()


# # TASK #7: COMPILE AND TRAIN DEEP CNN MODEL

# In[22]:


CNN.compile(optimizer = 'Adam', loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'])


# In[27]:


history = CNN.fit(X_train_gray_norm,
                 y_train,
                 batch_size = 1000,
                 epochs = 50,
                 verbose = 1,
                 validation_data = (X_validation_gray_norm, y_validation))


# # TASK #8: ASSESS TRAINED CNN MODEL PERFORMANCE 

# ![image.png](attachment:image.png)

# In[29]:


score = CNN.evaluate(X_test_gray_norm, y_test)
print('Test Accuracy: {}'.format(score[1]))


# In[30]:


history.history.keys()


# In[31]:


accuracy = history.history['accuracy']
val_accuracy = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']


# In[32]:


epochs = range(len(accuracy))
plt.plot(epochs, loss, 'ro', label = 'Training loss')
plt.plot(epochs, val_loss, 'r', label = 'Validation loss')
plt.title('Training and Validation loss')


# In[34]:


plt.plot(epochs, accuracy, 'ro', label = 'Training Accuracy')
plt.plot(epochs, val_accuracy, 'r', label = 'Validation Accuracy')
plt.title('Training and Validation Accuracy')


# In[ ]:





# In[35]:


predicted_classes = CNN.predict_classes(X_test_gray_norm)
y_true = y_test

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_true, predicted_classes)
plt.figure(figsize = (25, 25))
sns.heatmap(cm, annot = True)


# In[36]:


L = 5
W = 5

fig, axes = plt.subplots(L, W, figsize = (12, 12))
axes = axes.ravel()

for i in np.arange(0, L*W):
    axes[i].imshow(X_test[i])
    axes[i].set_title('Prediction = {}\n True = {}'.format(predicted_classes[i], y_true[i]))
    axes[i].axis('off')

plt.subplots_adjust(wspace = 1)    


# # CONGRATULATIONS ON FINISHING THE PROJECT!

# # APPENDIX

# - In this case study, we want to classify images of traffic signs using deep Convolutional Neural Networks (CNNs).
# - The dataset consists of 43 different classes of images. 
# - Classes are as listed below: 
#   - 0 = Speed limit (20km/h) 
#   - 1 = Speed limit (30km/h)
#   - 2 = Speed limit (50km/h) 
#   - 3 = Speed limit (60km/h)
#   - 4 = Speed limit (70km/h) 
#   - 5 = Speed limit (80km/h)
#   - 6 = End of speed limit (80km/h)
#   - 7 = Speed limit (100km/h)
#   - 8 = Speed limit (120km/h)
#   - 9 = No passing
#   - 10 = No passing for vehicles over 3.5 metric tons
#   - 11 = Right-of-way at the next intersection
#   - 12 = Priority road
#   - 13 = Yield
#   - 14 = Stop
#   - 15 = No vehicles
#   - 16 = Vehicles over 3.5 metric tons prohibited
#   - 17 = No entry
#   - 18 = General caution
#   - 19 = Dangerous curve to the left
#   - 20 = Dangerous curve to the right
#   - 21 = Double curve
#   - 22 = Bumpy road
#   - 23 = Slippery road
#   - 24 = Road narrows on the right
#   - 25 = Road work
#   - 26 = Traffic signals
#   - 27 = Pedestrians
#   - 28 = Children crossing 
#   - 29 = Bicycles crossing
#   - 30 = Beware of ice/snow
#   - 31 = Wild animals crossing
#   - 32 = End of all speed and passing limits
#   - 33 = Turn right ahead
#   - 34 = Turn left ahead
#   - 35 = Ahead only
#   - 36 = Go straight or right
#   - 37 = Go straight or left
#   - 38 = Keep right
#   - 39 = Keep left
#   - 40 = Roundabout mandatory
#   - 41 = End of no passing
#   - 42 = End of no passing by vehicles over 3.5 metric tons
# 
# - Citation
# J. Stallkamp, M. Schlipsing, J. Salmen, and C. Igel. The German Traffic Sign Recognition Benchmark: A multi-class classification competition. In Proceedings of the IEEE International Joint Conference on Neural Networks, pages 1453–1460. 2011. 
# @inproceedings{Stallkamp-IJCNN-2011, author = {Johannes Stallkamp and Marc Schlipsing and Jan Salmen and Christian Igel}, booktitle = {IEEE International Joint Conference on Neural Networks}, title = {The {G}erman {T}raffic {S}ign {R}ecognition {B}enchmark: A multi-class classification competition}, year = {2011}, pages = {1453--1460} }

# In[ ]:




