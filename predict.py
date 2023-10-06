# ======        for prediction using our trained model ============================================

from matplotlib import pyplot as plt
import os
import numpy as np
import matplotlib.image as img
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model

def predict(test_img_path):
    filepath = 'vgg-16-Tea-leaves-disease-model.hdf5'
    model = load_model(filepath)
    print(model)

    print("Model Loaded Successfully")

    test_image = load_img(test_img_path, target_size = (180,180)) # load image 

    test_image = img_to_array(test_image)#/255 # convert image to np array and normalize
    test_image = np.expand_dims(test_image, axis = 0)# change dimention 3D to 4D

    result = model.predict(test_image) # predict diseased palnt or not
    #print(result) 

    pred = np.argmax(result, axis=1)
    pred = pred[0]

    expression = ['Anthracnose', 'algal leaf', 'bird eye spot', 'brown blight', 'gray light', 'healthy', 'red leaf spot','white spot']

    test_image = img.imread(test_img_path)
    print(expression[pred])
    pred=expression[pred]
    # plt.imshow(test_image)
    return pred
# predict('uploads/UNADJUSTEDNONRAW_thumb_1.jpg')