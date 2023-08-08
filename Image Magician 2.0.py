import cv2
import cv2
import tkinter as tk
from tkinter import filedialog
import numpy as np
import os
from tkinter import colorchooser


brightness_value = 50  
saturation_value = 50
contrast_value=50
hue_shift_value = 0  
gamma_value=1.5
noise_correction_value = 0
adjusted_image = None  
original_image = None  # Image path, working on adding upload button
saturation_factor=2.5
crop_x, crop_y, crop_width, crop_height = 0, 0, 400, 300  # Initial crop parameters
rotate_angle = 0


def upload_image():
    global original_image
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")])   # Opening the image in tkinter and then passing the pass for cv2 window to perform operations
    if file_path: 
        original_image = cv2.imread(file_path)
        resize_image=cv2.resize(original_image,(400,300))
        original_image=resize_image
        cv2.imshow('Image Adjustments',original_image)


def update_brightness(val):
    global brightness_value
    brightness_value = val
    update_image()
    
def update_contrast(val):
    global contrast_value
    contrast_value = val
    update_image()

def update_saturation(val):
    global saturation_value
    saturation_value = val
    update_image()

def update_hue_shift(val):
    global hue_shift_value
    hue_shift_value = val
    update_image()

def update_noise_correction(val):
    global noise_correction_value
    noise_correction_value = val
    update_image()
    
def update_gamma(val):
    global gamma_value
    gamma_value = val / 10.0
    update_image()

def apply_gamma_correction(image, gamma):
    gamma_corrected = np.power(image / 255.0, gamma) * 255.0
    return np.uint8(gamma_corrected)
def update_crop(x, y, width, height):
    global crop_x, crop_y, crop_width, crop_height
    crop_x, crop_y, crop_width, crop_height = x, y, width, height
    update_image()



def crop_image():
    global original_image
    global adjusted_image
    if original_image is not None:
        cropped_image = original_image[crop_y:crop_y + crop_height, crop_x:crop_x + crop_width]
        adjusted_image = cropped_image.copy()
        cv2.imshow('Image Adjustments', adjusted_image)

def update_rotate(angle):
    global rotate_angle
    rotate_angle = angle
    update_image()

def rotate_image():
    global adjusted_image
    if original_image is not None:
        rows, cols, _ = original_image.shape
        rotation_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), rotate_angle, 1)
        adjusted_image = cv2.warpAffine(original_image, rotation_matrix, (cols, rows))
        cv2.imshow('Image Adjustments', adjusted_image)

    
def update_image():
    global adjusted_image
    if original_image is not None:
        hsv_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)
        hsv_image[..., 2] = cv2.convertScaleAbs(hsv_image[..., 2], alpha=brightness_value / 50.0)
        hsv_image[..., 2] = cv2.convertScaleAbs(hsv_image[..., 2], alpha=contrast_value / 50.0)
        hsv_image[..., 1] = cv2.convertScaleAbs(hsv_image[..., 1], alpha=saturation_value / 50.0)
        hsv_image[..., 0] = (hsv_image[..., 0] + hue_shift_value) % 180

        noise_mask = np.random.normal(0, noise_correction_value, hsv_image.shape[:2])
        hsv_image[..., 2] += noise_mask.astype(np.uint8)

        adjusted_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
        adjusted_image = apply_gamma_correction(adjusted_image, gamma_value)

        cv2.imshow('Image Adjustments', adjusted_image)
        
        
        
        # Apply Gaussian blur based on the current blur level
    else:
        print("Pass the image")
    cv2.imshow('Image Adjustments', adjusted_image)
    
def add_blur():
    global original_image
    global adjusted_image
    if adjusted_image is None:
    
        blurred_image=cv2.GaussianBlur(original_image,(5,5),0)
        cv2.imshow('Image Adjustments',blurred_image)
    else:
        
        blurred_image=cv2.GaussianBlur(adjusted_image,(5,5),0)
        cv2.imshow('Image Adjustments',blurred_image)
        

        
        
# Creating separate cv2 window and the trackbar to change different image options
cv2.namedWindow('Image Adjustments')
cv2.createTrackbar('Brightness', 'Image Adjustments', brightness_value, 100, update_brightness) # change brightness
cv2.createTrackbar('Saturation', 'Image Adjustments', saturation_value, 100, update_saturation) # change saturation
cv2.createTrackbar('Hue Shift', 'Image Adjustments', hue_shift_value, 180, update_hue_shift)    # Change Hue Shift
cv2.createTrackbar('Noise Correction', 'Image Adjustments', noise_correction_value, 50, update_noise_correction) # Change noise
cv2.createTrackbar('Contrast', 'Image Adjustments', contrast_value, 100, update_contrast)   # change contrast
cv2.createTrackbar('Gamma', 'Image Adjustments', 10, 30, update_gamma) 
cv2.createTrackbar('Crop X', 'Image Adjustments', 0, 400, lambda x: update_crop(x, crop_y, crop_width, crop_height))
cv2.createTrackbar('Crop Y', 'Image Adjustments', 0, 300, lambda y: update_crop(crop_x, y, crop_width, crop_height))
cv2.createTrackbar('Crop Width', 'Image Adjustments', 400, 400, lambda w: update_crop(crop_x, crop_y, w, crop_height))
cv2.createTrackbar('Crop Height', 'Image Adjustments', 300, 300, lambda h: update_crop(crop_x, crop_y, crop_width, h))
cv2.createTrackbar('Rotate', 'Image Adjustments', 0, 360, update_rotate)




def save_image():
    global original_image
    if original_image is not None:
        output_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        if output_path:

            cv2.imwrite(output_path, adjusted_image)
            
            with open('Adjusted_values.txt','w') as f:
                f.write('New Brightness Value '+str(brightness_value))
                f.write('\nNew Saturation Value '+str(saturation_value))
                f.write('\nNew Hue Shift Value '+str(hue_shift_value))
                f.write('\nNew Noise Correction Value '+str(noise_correction_value))

            print("Image saved successfully.")
            print('Document saved successfully')

original_image = None

root = tk.Tk()
root.title('Image Magician')
root.config(bg='grey')
root.geometry('600x900')

def exit():
    root.quit()

header_label = tk.Label(root, text='Welcome to Image Magician', font=("Helvetica", 16,'bold'), bg='grey')
header_label.pack(pady=10)
description_label=tk.Label(root,text='Change Brightness, Saturation, HUE And ETC Of Your Images',font=("Helvetica", 12,'bold'), bg='grey')
description_label.pack(pady=15)
info_label=tk.Label(root,text='Press Upload Image To Upload Your Image',font=("Helvetica", 12,'bold'), bg='grey')
info_label.pack(pady=20)
note_label=tk.Label(root,text="Press Save Image To Save The Image Along With New Information",font=("Helvetica", 12,'bold'), bg='grey')
note_label.pack(pady=25)
upload_button = tk.Button(root, text="Upload Image",font=("Helvetica", 12,'bold'), bg='grey',borderwidth=5, command=upload_image)
upload_button.pack(side='top')

save_button = tk.Button(root, text="Save Image",font=("Helvetica", 12,'bold'), bg='grey',borderwidth=5, command=save_image)
save_button.pack(pady=35)
Blur_button=tk.Button(root,text='Add Gaussian Blur ',font=("Helvetica", 12,'bold'), bg='grey',borderwidth=5, command=add_blur)
Blur_button.pack(pady=35)
crop_button = tk.Button(root, text="Crop Image", font=("Helvetica", 12,'bold'), bg='grey',borderwidth=5, command=crop_image)
crop_button.pack( pady=45)

rotate_button = tk.Button(root, text="Rotate Image", font=("Helvetica", 12,'bold'), bg='grey',borderwidth=5, command=rotate_image)
rotate_button.pack(pady=50)



exit_button=tk.Button(root,text='Quit ?',font=("Helvetica", 12,'bold'), bg='grey',borderwidth=5,command=exit)
exit_button.pack(side='bottom')


root.mainloop()
