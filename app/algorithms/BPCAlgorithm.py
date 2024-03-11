import numpy as np
# pip install numpy
from PIL import Image
# pip install pillow

def bpc_encode(image_path, message, save_path):
    # Open the image
    img = Image.open(image_path)
    img_array = np.array(img)

    # Convert the message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    # Append a unique termination pattern to the binary message
    termination_pattern = '1111111111111110'
    binary_message += termination_pattern

    # Check if the message can fit in the image
    if len(binary_message) > img_array.size:
        raise ValueError("Message is too large to fit in the image")

    # Encode the message into the LSB of each pixel's bit-plane
    bit_plane_complexity = np.zeros_like(img_array, dtype=np.uint8)
    for i in range(8):
        bit_plane = (img_array >> i) & 1
        bit_plane_complexity += (bit_plane << i)

    # Flatten the arrays for easier indexing
    flat_img = img_array.reshape(-1)
    flat_complexity = bit_plane_complexity.reshape(-1)

    for i, bit in enumerate(binary_message):
        flat_complexity[i] = (flat_complexity[i] & ~1) | int(bit)

    # Reshape back to the original image shape
    encoded_img_array = flat_complexity.reshape(img_array.shape)

    # Save the modified bit-plane complexity as a new image
    encoded_img = Image.fromarray(encoded_img_array)
    encoded_img.save(save_path, "PNG")

    print("Message encoded successfully.")
    
def bpc_decode(image_path):
    # Open the encoded image
    encoded_img = Image.open(image_path)
    encoded_img_array = np.array(encoded_img)

    # Extract the message from the LSB of each pixel's bit-plane
    binary_message = ""
    for i in range(8):
        bit_plane = (encoded_img_array >> i) & 1
        binary_message += ''.join(str(bit) for bit in bit_plane.flat)

    # Define a unique pattern to indicate the end of the message
    termination_pattern = '1111111111111110'

    # Find the index of the first occurrence of the termination pattern
    termination_index = binary_message.find(termination_pattern)

    # Extract the message up to the termination pattern
    binary_message = binary_message[:termination_index]

    print(binary_message    )
    # Convert binary message to ASCII
    message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        message += chr(int(byte, 2))

    return message

# # Example usage:
# # Encode a message into an image
# bpc_encode("input_image.png", "Hello, World!")

# # Decode the message from the encoded image
path1 = "D:/Projects/steganography-git/media/encoded/BPC__a22e197c-27df-499e-ae50-c19cf499928f.png"
path3 = "D:/Projects/steganography-git/media/encoded/BPC__9cd0c529-eba8-46b9-916a-9fc81c7398c5.jpg"

path2 = "D:/Projects/steganography-git/media/encoded/BPC__6415e80c-fc9d-4a95-afa9-4ecc49aaed6b.jpg"
# decoded_message = bpc_decode(path3)
# print("Decoded message:")
# print(decoded_message)
