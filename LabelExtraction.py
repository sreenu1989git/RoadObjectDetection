import os
from os import walk, getcwd
from PIL import Image
import json
from functools import partial
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')

make_directory = partial(os.makedirs, exist_ok=True)

# paths of images, json files, and labels.
img_folder = "C:/Users/sreenu/Downloads/bdd100k_images_100k/bdd100k/images/100k/" # path of folder where 'train', 'val', and 'test' image folders lie.
json_folder = "C:/Users/sreenu/Downloads/bdd100k_det_20_labels_trainval/bdd100k/labels/det_20/" # path of folder where 'train', 'val' json files lie.

train_img_path = img_folder+'train/'
val_img_path = img_folder+'val/'
test_img_path = img_folder+'test/'

train_json_file = json_folder+'det_train.json'
val_json_file = json_folder+'det_val.json'

# create a folder to save the text files of 'labels of training images' extracted from json file.
train_label_path = train_img_path.replace('images/', 'labels/') 
if not os.path.exists(train_label_path):
   make_directory(train_label_path)

# create a folder to save the text files of 'labels of validation images' extracted from json file.
val_label_path = val_img_path.replace('images/', 'labels/')
if not os.path.exists(val_label_path):
   make_directory(val_label_path)

# Class names for different categories of objects
classes = ['pedestrian', 'rider', 'car', 'truck', 'bus', 'train', 'motorcycle', 'bicycle', 'traffic light', 'traffic sign']

# function rectangle start and end coordinates (x1, y1, x2, y2) to rectangle origin, width, and height (x1, y1, w, h) as required by YOLO Object detction models
def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

# function to count the number files in folder
def file_list(folder_path):
   files = []
   for (dirpath, dirnames, filenames) in walk(folder_path):
      files.extend(filenames)
      break
   return files

# counting the number images for which labels are available in json file.
def lbld_img(json_file):
  labeled_images = []
  json_content = open(json_file, 'r')
  j_data = json.load(json_content)
  for file in tqdm(j_data):
    labeled_images.append(file['name'])
  return labeled_images

# function to delete the unwanted files.
def remove_files(folder_path, files_toRemove):
   for filename in tqdm(files_toRemove):
      if os.path.exists(folder_path+filename):
         os.remove(folder_path+filename)

# checking number of images in 'train' image folder.
print("Counting the total number of images in 'train' folder.")
train_img_list = file_list(train_img_path)
print("The total number of images available for training: "+ str(len(train_img_list)))

# checking number of labels in 'train' json file.
print("Counting the total number of training images for which labels are available.")
train_images_labeled = lbld_img(train_json_file)
print("The total number of training images for which labels are available: "+ str(len(train_images_labeled)))

# priting image file names for which labels are missing.
train_images_wol = set(train_img_list)-set(train_images_labeled)
print("The total number of training images for which labels are missing:" + str(len(train_images_wol)))

# removing images for which labels are missing.
if len(train_images_wol)>0:
   print("Removing the training images for which labels are missing:" + str(len(train_images_wol)))
   remove_files(train_img_path, train_images_wol)
   train_img_list = file_list(train_img_path)
   print("Total number of images available for training after removing the images \n for which labels are missing: "+ str(len(train_img_list)))

# checking number of images in 'validation' image folder.
print("Counting the total number of images in 'validation' folder.")
val_img_list = file_list(val_img_path)
print("The total number of images available for validation: "+ str(len(val_img_list)))

# checking number of labels in 'val' json file.
print("Counting the total number of validation images for which labels are available.")
val_images_labeled = lbld_img(val_json_file)
print("The total number of validation images for which labels are available: "+ str(len(val_images_labeled)))

# priting image file names for which labels are missing.
val_images_wol = set(val_img_list)-set(val_images_labeled)
print("Total number of validation images for which labels are missing:" + str(len(val_images_wol)))

# removing images for which labels are missing.
if len(val_images_wol)>0:
   print("Removing the validation images for which labels are missing:" + str(len(val_images_wol)))
   remove_files(val_img_path, val_images_wol)
   val_img_list = file_list(val_img_path)
   print("Total number of images available for validation after removing the images \n for which labels are missing: "+ str(len(train_img_list)))

# checking number of images in 'test' image folder.
print("Counting the total number of images in 'test' folder.")
test_img_list = file_list(test_img_path)
print("The total number of images available for testing: "+ str(len(test_img_list)))

def generate_labels(json_file, label_path, ext_status_file):
  
  # creating a text file to save the file names of images for label extraction completed.
  label_ext_completed = open(ext_status_file, 'a+')
  label_ext_completed.seek(0)
  labeled_files = label_ext_completed.readlines() # reading the file names of images for label extraction completed.
  
  # reading the json file for extraction of labels.
  json_content = open(json_file, 'r')
  j_data = json.load(json_content)


  # iterating through json objects to search for labels for images.
  for file in tqdm(j_data):
    if file['name']+'\n' not in labeled_files:
      """ Open output text files """
      txt_outpath = label_path + file['name'].replace('jpg','txt') # creating text files for saving label data of images with same file name.
      txt_outfile = open(txt_outpath, 'w')
    
      # checking if the labels are available for the image.
      if 'labels' in file:
        num_obj = len(file['labels'])
        
        # extracting class labels and bounding box coordinates from json as required by YOLO and writing to text files.
        for num in range(num_obj):
          cls = file['labels'][num]['category']
          if cls in classes:
            cls_id = classes.index(cls)
            xmin = file['labels'][num]['box2d']['x1']
            xmax = file['labels'][num]['box2d']['x2']
            ymin = file['labels'][num]['box2d']['y1']
            ymax = file['labels'][num]['box2d']['y2']

            box = (float(xmin), float(xmax), float(ymin), float(ymax))
            bb = convert((1280, 720), box)
            txt_outfile.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

      txt_outfile.close() # closing the label file.
    
    label_ext_completed.write(file['name'] + '\n')

  
  label_ext_completed.close() # closing Label Extraction completion status file.

print("Training label extraction started.")
generate_labels(train_json_file, train_label_path, 'Training Label Extraction Completed.txt')
print("Training label extraction completed.")

print("Validation label extraction started.")
generate_labels(val_json_file, val_label_path, 'Validation Label Extraction Completed.txt')
print("Validation label extraction completed.")