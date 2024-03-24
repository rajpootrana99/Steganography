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

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
import time
import cv2
import multiprocessing
import os
import sys

from steganography.settings import BASE_DIR

total_frames_saved = 0

def extract_frames(video_path, frames_dir, overwrite=False, start=-1, end=-1, every=1):
    """
    Extract frames from a video using OpenCVs VideoCapture
    :param video_path: path of the video
    :param frames_dir: the directory to save the frames
    :param overwrite: to overwrite frames that already exist?
    :param start: start frame
    :param end: end frame
    :param every: frame spacing
    :return: count of images saved
    """

    video_path = os.path.normpath(video_path)  # make the paths OS (Windows) compatible
    frames_dir = os.path.normpath(frames_dir)  # make the paths OS (Windows) compatible
    print("VIdeo Extraction Function: ", os.path.exists(video_path))
    video_dir, video_filename = os.path.split(video_path)  # get the video path and filename from the path

    assert os.path.exists(video_path)  # assert the video file exists

    capture = cv2.VideoCapture(video_path)  # open the video using OpenCV
    # print(capture)
    
    if start < 0:  # if start isn't specified lets assume 0
        start = 0
    if end < 0:  # if end isn't specified assume the end of the video
        end = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

    capture.set(1, start)  # set the starting frame of the capture
    frame = start  # keep track of which frame we are up to, starting from start
    while_safety = 0  # a safety counter to ensure we don't enter an infinite while loop (hopefully we won't need it)
    saved_count = 0  # a count of how many frames we have saved

    while frame < end:  # lets loop through the frames until the end

        _, image = capture.read()  # read an image from the capture

        if while_safety > 500:  # break the while if our safety maxs out at 500
            break

        # sometimes OpenCV reads None's during a video, in which case we want to just skip
        if image is None:  # if we get a bad return flag or the image we read is None, lets not save
            while_safety += 1  # add 1 to our while safety, since we skip before incrementing our frame variable
            continue  # skip

        if frame % every == 0:  # if this is a frame we want to write out based on the 'every' argument
            while_safety = 0  # reset the safety count
            save_path = os.path.join(frames_dir, f"{frame}.png")  # create the save path
            # print(save_path)
            if not os.path.exists(save_path) or overwrite:  # if it doesn't exist or we want to overwrite anyways
                cv2.imwrite(save_path, image)  # save the extracted image
                saved_count += 1  # increment our counter by one

        frame += 1  # increment our frame count

    print(frame)
    capture.release()  # after the while has finished close the capture

    return saved_count  # and return the count of the images we saved


def video_to_frames(message_len, video_path, frames_dir, overwrite=False, every=1, chunk_size=1000):
    """
    Extracts the frames from a video using multiprocessing
    :param video_path: path to the video
    :param frames_dir: directory to save the frames
    :param overwrite: overwrite frames if they exist?
    :param every: extract every this many frames
    :param chunk_size: how many frames to split into chunks (one chunk per cpu core process)
    :return: path to the directory where the frames were saved, or None if fails
    """

    video_path = os.path.normpath(video_path)  # make the paths OS (Windows) compatible
    frames_dir = os.path.normpath(frames_dir)  # make the paths OS (Windows) compatible
    print(frames_dir)
    print(video_path)
    video_dir, video_filename = os.path.split(video_path)  # get the video path and filename from the path

    # make directory to save frames, its a sub dir in the frames_dir with the video name
    os.makedirs(frames_dir, exist_ok=True)

    capture = cv2.VideoCapture(video_path)  # load the video
    total = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))  # get its total frame count
    capture.release()  # release the capture straight away

    
    if total < 1:  # if video has no frames, might be and opencv error
        print("Video has no frames. Check your OpenCV + ffmpeg installation")
        return 0  # return None
    elif message_len < total:
        total = message_len+1
        
    print(total)
    frame_chunks = [[i, i+chunk_size] for i in range(0, total, chunk_size)]  # split the frames into chunk lists
    frame_chunks[-1][-1] = min(frame_chunks[-1][-1], total-1)  # make sure last chunk has correct end frame, also handles case chunk_size < total

    prefix_str = "Extracting frames from {}".format(video_filename)  # a prefix string to be printed in progress bar
    print(prefix_str)
    print(frame_chunks)
    
    # Use ThreadPoolExecutor instead of ProcessPoolExecutor
    with ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        futures = [executor.submit(extract_frames, video_path, frames_dir, overwrite, f[0], f[1], every)
                   for f in frame_chunks]

        for future in as_completed(futures):
            result = future.result()
            print(result)

    return total


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
        
        frame_save_path = frame_save_path.replace("\\", "/")
        
        # video frames
        
        if not os.path.isdir(frame_save_path):
            os.makedirs(frame_save_path)
        total_frame = video_to_frames(secret_message_length, file_path, frame_save_path)
        
        # for index, frame in enumerate(video_object.iter_frames()):
        #     img = Image.fromarray(frame, 'RGB')
        #     img.save(f'{frame_save_path}/{index}.png')
        #     total_frame += 1
            
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
            frame_path = frame_path.replace("\\", "/")
            try:
                decoded_message += decoder(frame_path)
                print(f"Frame {index} message: {decoded_message}")
                # print("Data found in Frame %d" , frame_path)
            except StopIteration:
                print("No data found in Frame %d", frame_path)
        print("\nExtraction Complete!")
        if decoded_message[len(decoded_message)-4:] == "m20;":
           decoded_message = decoded_message[:len(decoded_message)-4]
        return decoded_message
    
    except:
        return 'No Data Found'





# Example usage:
# print(BASE_DIR)
video_path = str(BASE_DIR).replace("\\", "/") + "/static/assets/samples/500kb.mp4"
print(video_path)
output_path =  str(BASE_DIR).replace("\\", "/") + "/static/assets/samples/frames"
text_to_hide = "Hello, world!"
# text_to_hide = "It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like)."


start_time = time.time()
# # print(video_to_frames(video_path, output_path))
encode(video_path, text_to_hide, output_path)
print("--- %s seconds ---" % (time.time() - start_time))



start_time = time.time()
print("Decoded Message:", decode(output_path))
print("--- %s seconds ---" % (time.time() - start_time))
exit(0)