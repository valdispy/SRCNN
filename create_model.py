# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 00:12:47 2019

@author: valdis
"""
import cv2, glob
import numpy as np
from keras.models import Sequential
from keras.layers import Convolution2D
from keras.optimizers import Adam

def create_datasets(work_folder, need_scale_value): 
    X_train_list = []; Y_train_list = []
    work_folder_list = glob.glob(work_folder + '/*/*.jpeg')
    
    print('Creating datasets ...')
    for image_path in work_folder_list: 
        if '_upscale_' + str(need_scale_value) in image_path: 
            X_train_list.append(image_path)
        elif '_upscale_' not in image_path:
            Y_train_list.append(image_path) 
    
    X_train_data = np.array([cv2.imread(file) for file in X_train_list])   
    Y_train_data = np.array([cv2.imread(file) for file in Y_train_list])   
    return X_train_data, Y_train_data

if __name__ == "__main__":
    
    need_scale_value = 4
    work_folder = '/home/valdis/Desktop/SR_folder/upscale_folder'    
    
    X_train_data, Y_train_data = create_datasets(work_folder, need_scale_value) 
    
    model = Sequential()
    _, height, width, channels = X_train_data.shape
    optimizer = Adam(learning_rate = 0.001, beta_1 = 0.9, beta_2 = 0.999, amsgrad = False)
    model.add(Convolution2D(filters = 64, kernel_size = (9, 9), padding = 'same', input_shape = (height, width, channels), activation = 'relu'))
    model.add(Convolution2D(filters = 32, kernel_size = (1, 1), padding = 'same', activation = 'relu'))
    model.add(Convolution2D(filters = channels, padding = 'same', kernel_size = (5, 5)))
    model.compile(optimizer, 'mse')
    
    model.fit(X_train_data, Y_train_data, batch_size=32, epochs=15)
    model.save('model.h5')
    
    print(model.summary())