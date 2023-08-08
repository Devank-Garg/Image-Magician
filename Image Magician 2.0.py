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

def update_saturation_factor(val):
    global saturation_factor
    saturation_factor = val / 10.0
    add_color_saturation()
    
def pick_color_and_get_range(image_path):
    def mouse_callback(event, x, y, flags, param):
        nonlocal colorsRGB, stop_display
        if event == cv2.EVENT_LBUTTONDOWN:
            colorsBGR = image[y, x]
            colorsRGB = tuple(reversed(colorsBGR))
            stop_display = True

    image = cv2.imread(image_path)
    image = cv2.resize(image, (400, 400))

    cv2.namedWindow('PickColorAndGetRange')
    cv2.setMouseCallback('PickColorAndGetRange', mouse_callback)

    colorsRGB = None
    stop_display = False

    while not stop_display:
        cv2.imshow('PickColorAndGetRange', image)
        if cv2.waitKey(10) & 0xFF == 27:
            break

    cv2.destroyWindow('PickColorAndGetRange')
    if colorsRGB is not None:
        picked_color_hsv = cv2.cvtColor(np.uint8([[colorsRGB]]), cv2.COLOR_BGR2HSV)
        hue_range = 15
        color_range = (picked_color_hsv[0][0][0] - hue_range, 40, 40), (picked_color_hsv[0][0][0] + hue_range, 255, 255)
        return color_range
    else:
        return None

def change_color_saturation(image, color_range, saturation_factor):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_bound = np.array(color_range[0], dtype=np.uint8)
    upper_bound = np.array(color_range[1], dtype=np.uint8)

    mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

    h, s, v = cv2.split(hsv_image)

    s[mask > 0] = np.clip(s[mask > 0] * saturation_factor, 0, 255)
    hsv_image = cv2.merge([h, s, v])

    output_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

    return output_image


def choose_color():
    global color_range, saturation_factor
    color_code = colorchooser.askcolor(title="Choose color")
    if color_code[1] is not None:
        picked_color_hsv = cv2.cvtColor(np.uint8([[color_code[0]]]), cv2.COLOR_BGR2HSV)
        hue_range = 15  
        color_range = (picked_color_hsv[0][0][0] - hue_range, 40, 40), (picked_color_hsv[0][0][0] + hue_range, 255, 255)
        add_color_saturation()
        
def choose_color2():
    global color_range

    color_range = pick_color_and_get_range(file_path) 
    add_color_saturation()
    

    
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
        
        # Apply gamma correction
        adjusted_image = apply_gamma_correction(adjusted_image, gamma_value)
        
        
        
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
        
def add_color_saturation():
        global original_image
        global adjusted_image
        global color_range, saturation_factor
        if adjusted_image is None:
            color_image=change_color_saturation(original_image, color_range, saturation_factor)
            color_image=cv2.resize(color_image, (400, 300))
            cv2.imshow("Image Adjustments",color_image)
        else:
            
            modified_image = change_color_saturation(adjusted_image, color_range, saturation_factor)
            modified_image_resized = cv2.resize(modified_image, (400, 400))
            cv2.imshow("Image Adjustments",modified_image_resized)
            

        
        
    

    

    
  

# Creating separate cv2 window and the trackbar to change different image options
cv2.namedWindow('Image Adjustments')
cv2.createTrackbar('Brightness', 'Image Adjustments', brightness_value, 100, update_brightness) # change brightness
cv2.createTrackbar('Saturation', 'Image Adjustments', saturation_value, 100, update_saturation) # change saturation
cv2.createTrackbar('Hue Shift', 'Image Adjustments', hue_shift_value, 180, update_hue_shift)    # Change Hue Shift
cv2.createTrackbar('Noise Correction', 'Image Adjustments', noise_correction_value, 50, update_noise_correction) # Change noise
cv2.createTrackbar('Contrast', 'Image Adjustments', contrast_value, 100, update_contrast)   # change contrast
cv2.createTrackbar('Gamma', 'Image Adjustments', 10, 30, update_gamma) 
cv2.createTrackbar('Saturation Factor', 'Image Adjustments', int(saturation_factor*10) , 50, update_saturation_factor)


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

color_button=tk.Button(root,text='Pick Colour ',font=("Helvetica", 12,'bold'), bg='grey',borderwidth=5, command=choose_color)
color_button.pack(pady=40)
color_button2=tk.Button(root,text='Pick Colour from Image',font=("Helvetica", 12,'bold'), bg='grey',borderwidth=5, command=choose_color2)
color_button2.pack(pady=45)

exit_button=tk.Button(root,text='Quit ?',font=("Helvetica", 12,'bold'), bg='grey',borderwidth=5,command=exit)
exit_button.pack(side='bottom')


root.mainloop()