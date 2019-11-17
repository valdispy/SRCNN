# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 20:40:50 2019

@author: valdis
"""
import os, glob, cv2
import pandas as pd

def image_frame(image_list, column_names): 
    shape_list = []
    
    print('Processing (image frame) ...')
    for image_path in image_list: 
        image = cv2.imread(image_path)
        shape_list.append(list(image.shape) + [image_path])
    shape_frame = pd.DataFrame(shape_list, columns=column_names)
    return shape_frame
 
def crop_and_save(crop_folder, pass_path):
    image_min_height = pass_frame['height'].min()
    image_min_width = pass_frame['width'].min()
    
    print('Croping (pass frame) ...')
    for image_path in pass_path: 
        image = cv2.imread(image_path)
        crop_image = image[0:image_min_height, 0:image_min_width]
        
        base_name = os.path.basename(image_path)
        crop_path = os.path.join(crop_folder, base_name)
        cv2.imwrite(crop_path, crop_image)
    
    number_of_images = len(glob.glob(crop_folder + '/*.jpg'))
    return True if number_of_images == len(pass_path) else False
    
if __name__ == "__main__":

    min_height = 500; max_height = 1000
    column_names = ['height', 'width', 'channels', 'path']
    
    work_dir = os.getcwd()
    flickr_folder = os.path.join(work_dir, 'flickr_folder')
    crop_folder = os.path.join(work_dir, 'crop_folder')
    
    if os.path.exists(crop_folder) == False: 
        os.mkdir(crop_folder)
    
    image_list = glob.glob(flickr_folder + '/*.jpg')
    shape_frame = image_frame(image_list, column_names)
    
    pass_frame = shape_frame[(shape_frame['height'] >= min_height) & (shape_frame['height'] <= max_height) &
                             (shape_frame['width'] >= shape_frame['height']) & (shape_frame['channels'] == 3)]
    
    pass_path = pass_frame['path'].tolist()
    
    status = 'Everything is fine !!!' if crop_and_save(crop_folder, pass_path) else "'photo of evil manul'" 
    print(status)