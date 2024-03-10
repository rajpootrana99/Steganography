import numpy as np
# pip install numpy
import cv2
# pip install opencv-python
from PIL import Image

def hide_message(image_path, message, save_path):
    img = cv2.imread(image_path)
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    # Add a unique termination signal
    binary_message += '1111111111111110101010101010101'

    # Flatten the image array
    img_flat = img.flatten()

    for i, bit in enumerate(binary_message):
        pixel_value = img_flat[i]
        pixel_value = pixel_value & ~1 | int(bit)
        img_flat[i] = pixel_value

    img_hidden = img_flat.reshape(img.shape)
    cv2.imwrite(save_path, img_hidden)

    print("Message hidden successfully.")
    return save_path

def reveal_message(hidden_image_path):
    hidden_img = cv2.imread(hidden_image_path)
    hidden_img_flat = hidden_img.flatten()

    binary_message = ""

    for pixel_value in hidden_img_flat:
        bit = pixel_value & 1
        binary_message += str(bit)

    # Find the index of the termination signal
    termination_index = binary_message.find('1111111111111110')

    # Ensure the termination signal is found
    if termination_index == -1:
        raise ValueError("Termination signal not found in the encoded message")

    # Get the binary message without the termination signal
    binary_message_without_termination = binary_message[:termination_index]

    # Split the binary message into 8-bit chunks
    message_chunks = [binary_message_without_termination[i:i+8] for i in range(0, len(binary_message_without_termination), 8)]

    # Convert chunks to ASCII
    message = ''.join([chr(int(chunk, 2)) for chunk in message_chunks])

    return message


# # Example usage
# image_path = 'original_image.png'
# secret_message = "Hello, this is a secret message!"

# # Hide the message in the image
# hide_message(image_path, secret_message)


path1 = "D:/Projects/steganography-git/media/encoded/DFT__7d4be6cd-4dad-4829-9844-d32c9b6574d2.png"
path3 = "D:/Projects/steganography-git/media/encoded/DFT__0e15b516-32b7-4e00-8f88-5ef72fc5462c.jpg"

# # Reveal the hidden message from the image
# revealed_message = reveal_message(path3)
# print("Revealed message:")
# print(revealed_message)
