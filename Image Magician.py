import cv2
import tkinter as tk
from tkinter import filedialog
import numpy as np
import os

brightness_value = 50  
saturation_value = 50
hue_shift_value = 0  
noise_correction_value = 0
adjusted_image = None  
original_image = None  # Image path, working on adding upload button

def upload_image():
    global original_image
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

def update_image():
    global adjusted_image  # Global because we are calling it while running cv2 window loop
    if original_image is not None:
        hsv_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)
        hsv_image[..., 2] = cv2.convertScaleAbs(hsv_image[..., 2], alpha=brightness_value / 50.0)
        hsv_image[..., 1] = cv2.convertScaleAbs(hsv_image[..., 1], alpha=saturation_value / 50.0)
        hsv_image[..., 0] = (hsv_image[..., 0] + hue_shift_value) % 180
        
        noise_mask = np.random.normal(0, noise_correction_value, hsv_image.shape[:2])
        hsv_image[..., 2] += noise_mask.astype(np.uint8)
        adjusted_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
    else:
        print("Pass the image")
    cv2.imshow('Image Adjustments', adjusted_image)
# Creating separate cv2 window and the trackbar to change different image options
cv2.namedWindow('Image Adjustments')
cv2.createTrackbar('Brightness', 'Image Adjustments', brightness_value, 100, update_brightness)
cv2.createTrackbar('Saturation', 'Image Adjustments', saturation_value, 100, update_saturation)
cv2.createTrackbar('Hue Shift', 'Image Adjustments', hue_shift_value, 180, update_hue_shift)
cv2.createTrackbar('Noise Correction', 'Image Adjustments', noise_correction_value, 50, update_noise_correction)

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
root.geometry('600x450')

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
def exit():
    root.quit()
exit_button=tk.Button(root,text='Quit ?',font=("Helvetica", 12,'bold'), bg='grey',borderwidth=5,command=exit)
exit_button.pack(side='bottom')


root.mainloop()
