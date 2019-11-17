# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 00:12:47 2019

@author: valdis
"""

import cv2
import numpy as np
from keras.models import load_model

def predict_image(model, image_path): 
    
    model_input_shape = model.layers[0].input_shape[1:] 
    
    height, width, _ = model_input_shape 
    image = cv2.imread(image_path)[0:height, 0:width]    
    image_input_shape = image.shape
    
    if image_input_shape == model_input_shape: 
        predicted_image = model.predict(np.array([image]))
        normalized_image = cv2.normalize(predicted_image, None, alpha = 0, beta = 255,
                                     norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_8U)[0]
        print('Predicted image ready !!!')
    else: 
        normalized_image = image
        print('Image size mismatch !!!')
        
    return image, normalized_image

if __name__ == "__main__":
    
    model_path = 'model.h5'; predict_image_path = 'predicted_image.jpg'
    upscale_image_path = 'upscale_image.jpeg'; original_image_path = 'original_image.jpg'
    merge_image_path = 'concatenated_image.jpg'
       
    model = load_model(model_path)
    upscaled_image, predicted_image = predict_image(model, upscale_image_path)  
    cv2.imwrite(predict_image_path, predicted_image)
    
    original_image = cv2.imread(original_image_path)
    concatenated_image = np.concatenate((original_image, upscaled_image, predicted_image), axis=1)
    cv2.imwrite(merge_image_path, concatenated_image)