import numpy as np
# pip install numpy
import cv2
# pip install opencv-python

# Function to embed the secret message into the cover image using a spreading sequence
def embed_message(image_path, secret_message, save_path):
    try:
        cover_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
        if len(secret_message) > cover_image.size:
            raise ValueError("Secret message is too large to embed in the cover image.")

        # Set a seed for reproducibility (optional)
        np.random.seed(42)
        # Generate a random spreading sequence
        spreading_sequence = np.random.choice([-1, 1], cover_image.size)
    
        # Normalize cover image pixel values
        cover_image_normalized = cover_image.astype(np.float32) / 255.0

        spreaded_image = cover_image_normalized.copy().flatten()

        for i in range(len(secret_message)):
            binary_char = format(ord(secret_message[i]), '08b')  # Convert character to binary
            for j in range(8):
                spreaded_image[i * 8 + j] += spreading_sequence[i * 8 + j] * (int(binary_char[j]) - 0.5) * 2

        spreaded_image = np.clip(spreaded_image, 0, 1).reshape(cover_image.shape) * 255
        spreaded_image = spreaded_image.astype(np.uint8)

        # Save the steganographic image
        return cv2.imwrite(save_path, spreaded_image)
    except:
        return False

# Function to extract the secret message from the spreaded image using the spreading sequence
def extract_message(image_path, original_image_path, message_length):
    try:
        spreaded_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        cover_image = cv2.imread(original_image_path, cv2.IMREAD_GRAYSCALE)
        
        
        # Set a seed for reproducibility (optional)
        np.random.seed(42)
        # Generate a random spreading sequence
        spreading_sequence = np.random.choice([-1, 1], cover_image.size)
        
        extracted_message = ""

        spreaded_image_normalized = spreaded_image.astype(np.float32) / 255.0
        spreaded_image_flattened = spreaded_image_normalized.flatten()

        for i in range(message_length):
            binary_char = ''
            for j in range(8):
                bit = (spreaded_image_flattened[i * 8 + j] - 0.5) * 2 * spreading_sequence[i * 8 + j]
                if bit >= 0:
                    binary_char += '1'
                else:
                    binary_char += '0'
            extracted_message += chr(int(binary_char, 2))  # Convert binary to character

        return extracted_message
    except:
        return 'No Data Found'

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
