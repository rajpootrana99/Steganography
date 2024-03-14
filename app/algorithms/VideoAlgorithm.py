import glob
from stegano import lsb
from PIL import Image
import sys
import os, math
import cv2
import numpy as np
from PIL import Image
from moviepy.editor import *
from steganography.settings import *
import time, re

# Convert encoding data into 8-bit binary ASCII
def generateData(data):
    newdata = []
    for i in data: # list of binary codes of given data
        newdata.append(format(ord(i), '08b'))
    return newdata
 
# Pixels modified according to encoding data in generateData
def modifyPixel(pixel, data):
    datalist = generateData(data)
    lengthofdata = len(datalist)
    imagedata = iter(pixel)
    for i in range(lengthofdata):
        # Extracts 3 pixels at a time
        pixel = [value for value in imagedata.__next__()[:3] + imagedata.__next__()[:3] + imagedata.__next__()[:3]]
        # Pixel value should be made odd for 1 and even for 0
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pixel[j]% 2 != 0):
                pixel[j] -= 1
            elif (datalist[i][j] == '1' and pixel[j] % 2 == 0):
                if(pixel[j] != 0):
                    pixel[j] -= 1
                else:
                    pixel[j] += 1
        # Eighth pixel of every set tells whether to stop ot read further. 0 means keep reading; 1 means thec message is over.
        if (i == lengthofdata - 1):
            if (pixel[-1] % 2 == 0):
                if(pixel[-1] != 0):
                    pixel[-1] -= 1
                else:
                    pixel[-1] += 1
        else:
            if (pixel[-1] % 2 != 0):
                pixel[-1] -= 1
        pixel = tuple(pixel)
        yield pixel[0:3]
        yield pixel[3:6]
        yield pixel[6:9]
 
# take frame or image and encode data on it
def encoder(newimage, data):
    w = newimage.size[0]
    (x, y) = (0, 0)
 
    for pixel in modifyPixel(newimage.getdata(), data):
 
        # Putting modified pixels in the new image
        newimage.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1
 
# Improved Encoding Function
# Instead of performing Steganography on all the frames, the function will now instead perform Steganography on selected range of frames
def encode(file_path, secret_message, frame_save_path):
    try:
        secret_message_length = len(secret_message)
        
        """Returns all frames in the video object"""
        total_frame = 0
        video_object = VideoFileClip(file_path)
        if not os.path.isdir(frame_save_path):
            os.makedirs(frame_save_path)
        for index, frame in enumerate(video_object.iter_frames()):
            img = Image.fromarray(frame, 'RGB')
            img.save(f'{frame_save_path}/{index}.png')
            total_frame += 1
            
        # when have to embed through text file
        # try:
        #     with open(filename) as fileinput: # Store Data to be Encoded
        #         secret_message = fileinput.read()
        # except FileNotFoundError:
        #     print("\nFile to hide not found! Exiting...")
        #     quit()
        datapoints = math.ceil(secret_message_length / total_frame) # Data Distribution per Frame
        counter = 0
        print("Performing Steganography...")
        for convnum in range(0, secret_message_length, datapoints):
            numbering = frame_save_path + "/" + str(counter) + ".png"
            encodetext = secret_message[convnum:convnum+datapoints] # Copy Distributed Data into Variable
            try:
                image = Image.open(numbering, 'r') # Parameter has to be r, otherwise ValueError will occur (https://pillow.readthedocs.io/en/stable/reference/Image.html)
            except FileNotFoundError:
                print("\n%d.png not found! Exiting..." % counter)
                quit()
            newimage = image.copy() # New Variable to Store Hiddend Data
            encoder(newimage, encodetext) # Steganography
            new_img_name = numbering # Frame Number
            newimage.save(new_img_name, "PNG") # Save as New Frame
            counter += 1
        print("Complete!\n")
        print(f"Encoding Taken Time: {total_frame} ")
    except Exception as ex:
        print(ex)
        return False
    return True

    



# Decode the data in the image
def decoder(frame_path):
    data = ''
    # numbering = str(number)
    # decoder_numbering = frame_location + "\\" + numbering + ".png"
    decoder_numbering = frame_path
    image = Image.open(decoder_numbering, 'r')
    imagedata = iter(image.getdata())
    print(image)
    while (True):
        pixels = [value for value in imagedata.__next__()[:3] + imagedata.__next__()[:3] + imagedata.__next__()[:3]]
        # string of binary data
        binstr = ''
        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'
        if re.match("[ -~]", chr(int(binstr,2))) is not None: # only decode printable data
            data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data

def decode(frame_save_path):
    try:
        decoded_message = ''
        total_frames = len(glob.glob(f"{frame_save_path}/*.png"))
        for index in range(0, total_frames):
            frame_path = frame_save_path + "/" + str(index) + ".png"
            # print(frame_path)
            # frame_path = frame_path.replace("\\", "/")
            try:
                decoded_message += decoder(frame_path)
                print("Data found in Frame %d" , frame_path)
            except StopIteration:
                print("No data found in Frame %d", frame_path)
        print("\nExtraction Complete!")
        return decoded_message
    
    except:
        return 'No Data Found'


# Example usage:
# print(BASE_DIR)
# video_path = str(BASE_DIR).replace("\\", "/") + "/static/assets/samples/mp4.mp4"
# print(video_path)
# output_path =  str(BASE_DIR).replace("\\", "/") + "/static/assets/samples/frames"
# # # text_to_hide = "Hello, world!"
# text_to_hide = "It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like)."


# start_time = time.time()
# encode(video_path, text_to_hide, output_path)
# print("--- %s seconds ---" % (time.time() - start_time))

# start_time = time.time()
# print("Decoded Message:", decode(output_path))
# print("--- %s seconds ---" % (time.time() - start_time))
