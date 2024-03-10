import numpy as np
# pip install numpy
import cv2
# pip install opencv-python

def message_to_binary(message):
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    return binary_message

def binary_to_message(binary_message):
    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        message += chr(int(byte, 2))
    return message

# Function to spread the secret message into the cover image using a spreading sequence
def embed_message(image_path, message, save_path):
    cover_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    message = message_to_binary(message)# Generate a random spreading sequence (make sure to save this for extraction)
    # Set a seed for reproducibility (optional)
    np.random.seed(42)

    # Generate a random spreading sequence
    spreading_sequence = np.random.choice([-1, 1], cover_image.size)
    

    if len(message) > cover_image.size:
        raise ValueError("Secret message is too large to embed in the cover image.")

    spreaded_image = cover_image.copy()

    message = [int(bit) for bit in message]

    for i in range(len(message)):
        row, col = divmod(i, cover_image.shape[1])
        if message[i] == 0:
            spreaded_image[row, col] -= spreading_sequence[i]
        else:
            spreaded_image[row, col] += spreading_sequence[i]

    # Save the steganographic image
    cv2.imwrite(save_path, spreaded_image)
    
    return spreading_sequence

    

# Function to extract the secret message from the spreaded image using the spreading sequence
def extract_message(image_path, original_image_path, message_length):
    spreaded_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    cover_image = cv2.imread(original_image_path, cv2.IMREAD_GRAYSCALE)
    # Set a seed for reproducibility (optional)
    np.random.seed(42)

    # Generate a random spreading sequence
    spreading_sequence = np.random.choice([-1, 1], cover_image.size)
    
    extracted_message = ""

    for i in range(message_length):
        row, col = divmod(i, spreaded_image.shape[1])
        if spreaded_image[row, col] >= 0:
            extracted_message += '1'
        else:
            extracted_message += '0'

    print(extracted_message)
    extracted_message = binary_to_message(extracted_message)
    return extracted_message

# # Path to the cover image
# cover_image_path = "cover_image.jpg"

# # Generate a random spreading sequence (make sure to save this for extraction)
# spreading_sequence = np.random.choice([-1, 1], cv2.imread(cover_image_path, cv2.IMREAD_GRAYSCALE).size)

# # Secret message to embed
# secret_message = "0101010101"

# # Embed the message into the cover image
# spreaded_image = embed_message(cover_image_path, secret_message, spreading_sequence)

# # Save the steganographic image
# cv2.imwrite("steganographic_image.jpg", spreaded_image)

# # Extract the message from the steganographic image
# extracted_message = extract_message("steganographic_image.jpg", spreading_sequence, len(secret_message))

# print("Original Message:", secret_message)
# print("Extracted Message:", extracted_message)

# # Load a cover image
# cover_image = cv2.imread("cover_image.jpg", cv2.IMREAD_GRAYSCALE)

# # Generate a random spreading sequence (make sure to save this for extraction)
# spreading_sequence = np.random.choice([-1, 1], cover_image.size)

# # Secret message to embed
# secret_message = "0101010101"

# # Embed the message into the cover image
# spreaded_image = embed_message(cover_image, secret_message, spreading_sequence)

# # Save the steganographic image
# cv2.imwrite("steganographic_image.jpg", spreaded_image)


path1 = "D:/Projects/steganography-git/media/encoded/SS__ef18429c-91f1-4fb6-9d10-baab8d6c9c00.png"
path3 = "D:/Projects/steganography-git/media/encoded/SS__f3befb4d-b322-4f20-b517-5f1ae240b82d.jpg"


opath1 = "D:/Projects/steganography-git/media/original/SS__ef18429c-91f1-4fb6-9d10-baab8d6c9c00.png"
opath3 = "D:/Projects/steganography-git/media/original/SS__f3befb4d-b322-4f20-b517-5f1ae240b82d.jpg"

# # Extract the message from the steganographic image
# extracted_message = extract_message(path3, opath3, len("Muhammad Bin Zulfiqar"))


# # print("Original Message:", secret_message)
# print("Extracted Message:", extracted_message)
