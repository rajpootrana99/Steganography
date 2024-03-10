# import binascii
# from math import floor
# import numpy as np
# import cv2
# pad_h = None

# pad_w = None



# def pad_for_dct(img):
#     """Pads an image to ensure divisibility by 8 for DCT processing.

#     Args:
#         img (np.ndarray): The image to be padded.

#     Returns:
#         np.ndarray: The padded image.
#     """

#     h, w = img.shape[:2]
#     pad_h = (8 - h % 8) % 8  # Calculate padding for height
#     pad_w = (8 - w % 8) % 8  # Calculate padding for width

#     return cv2.copyMakeBorder(img, pad_h // 2, (pad_h + 1) // 2, pad_w // 2, (pad_w + 1) // 2, cv2.BORDER_CONSTANT, value=[0, 0, 0])  # Pad with zeros
# def embed_message(image_path, message, save_path):
#     img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE).astype(np.float32)

#     # Pad the image if necessary
#     padded_img = pad_for_dct(img)

#     # Apply DCT to the image
#     dct_img = cv2.dct(padded_img)

#     # Convert message to binary
#     binary_message = ''.join(format(ord(char), '08b') for char in message)

#     # Ensure message can fit within the image
#     max_message_length = dct_img.shape[0] * dct_img.shape[1] // 64  # Adjust as needed
#     if len(binary_message) > max_message_length:
#         raise ValueError("Message too long to be hidden effectively.")

#     # Divide image into 8x8 blocks
#     blocks = dct_img.reshape((dct_img.shape[0] // 8, 8, dct_img.shape[1] // 8, 8))

#     # Embed message bits into selected DCT coefficients (e.g., lower frequencies)
#     bit_index = 0
#     for i in range(blocks.shape[0]):
#         for j in range(blocks.shape[1]):
#             for k in range(8):
#                 for l in range(8):
#                     if bit_index < len(binary_message):
#                         blocks[i, j, k, l] = (blocks[i, j, k, l] // 2) * 2 + int(binary_message[bit_index])
#                         bit_index += 1
#                     else:
#                         break
#                 if bit_index == len(binary_message):
#                     break
#             if bit_index == len(binary_message):
#                 break
#         if bit_index == len(binary_message):
#             break

#     # Apply inverse DCT to reconstruct the image
#     idct_img = cv2.idct(blocks.reshape(dct_img.shape))

#     # Remove padding (if used)
#     if img.shape != idct_img.shape:
#         idct_img = idct_img[pad_h // 2:-pad_h // 2, pad_w // 2:-pad_w // 2]

#     # Convert back to uint8 for image display
#     idct_img = idct_img.astype(np.uint8)

#     # Save the steganographed image
#     cv2.imwrite(save_path, idct_img)

#     print("Message embedded successfully in the image.")
#     return save_path
#     img = cv2.imread(image_path, cv2.IMREAD_COLOR)

#     # Convert the message to binary
#     binary_message = ''.join(format(ord(char), '08b') for char in message)

#     # Add a unique termination signal
#     binary_message += '1111111111111110101010101010101'

#     # Pad the image for DCT processing
#     padded_img = pad_for_dct(img)
#     img_float = padded_img.astype(np.float32)

#     # Divide the image into 8x8 blocks
#     blocks = img_float.reshape((img_float.shape[0] // 8, 8, img_float.shape[1] // 8, 8))

#     # Apply DCT to each block
#     dct_blocks = np.zeros_like(blocks)
#     for i in range(blocks.shape[0]):
#         for j in range(blocks.shape[1]):
#             dct_blocks[i, j] = cv2.dct(blocks[i, j])

#     # Embed message bits into selected DCT coefficients
#     bit_index = 0
#     for i in range(blocks.shape[0]):
#         for j in range(blocks.shape[1]):
#             for k in range(4):  # Modify the first 4 coefficients in each block
#                 dct_blocks[i, j, 0, k] = (dct_blocks[i, j, 0, k] // 2) * 2 + int(binary_message[bit_index])
#                 bit_index += 1
#                 if bit_index == len(binary_message):
#                     break
#             if bit_index == len(binary_message):
#                 break

#     # Apply inverse DCT to reconstruct blocks
#     idct_blocks = np.zeros_like(blocks)
#     for i in range(blocks.shape[0]):
#         for j in range(blocks.shape[1]):
#             idct_blocks[i, j] = cv2.idct(dct_blocks[i, j])

#     # Reshape blocks back into the image
#     modified_img = idct_blocks.reshape(img_float.shape)

#     # Remove padding (if used)
#     if img_float.shape != modified_img.shape:
#         modified_img = modified_img[pad_h // 2:-pad_h // 2, pad_w // 2:-pad_w // 2]

#     # Convert back to uint8 for image display
#     modified_img = modified_img.astype(np.uint8)
#     cv2.imwrite(save_path, modified_img)
#     return
#     """Encodes a message into an image using DCT."""
#     img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
#     padded_img = pad_for_dct(img)
#     img_float = padded_img.astype(np.float32)

#     binary_message = ''.join(format(ord(char), '08b') for char in message)
#     max_message_length = img_float.shape[0] * img_float.shape[1] // 64
#     print("Binary Message:", binary_message)
#     if len(binary_message) > max_message_length:
#         raise ValueError("Message too long to be hidden effectively.")

#     blocks = img_float.reshape((img_float.shape[0] // 8, 8, img_float.shape[1] // 8, 8))
#     dct_blocks = np.zeros_like(blocks)

#     for i in range(blocks.shape[0]):
#         for j in range(blocks.shape[1]):
#             dct_blocks[i, j] = cv2.dct(blocks[i, j])

#     bit_index = 0

#     for i in range(blocks.shape[0]):
#         for j in range(blocks.shape[1]):
#             for k in range(4):
#                 dct_blocks[i, j, 0, k] = (dct_blocks[i, j, 0, k] // 2) * 2 + int(binary_message[bit_index])
#                 bit_index += 1
#                 if bit_index == len(binary_message):
#                     break
#             if bit_index == len(binary_message):
#                 break
#         if bit_index == len(binary_message):
#             break

#     idct_blocks = np.zeros_like(blocks)

#     for i in range(blocks.shape[0]):
#         for j in range(blocks.shape[1]):
#             idct_blocks[i, j] = cv2.idct(dct_blocks[i, j])

#     modified_img = idct_blocks.reshape(img_float.shape)

#     if img_float.shape != modified_img.shape:
#         modified_img = modified_img[pad_h // 2:-pad_h // 2, pad_w // 2:-pad_w // 2]

#     modified_img = modified_img.astype(np.uint8)
#     cv2.imwrite(save_path, modified_img)

# def extract_message(image_path):
#     img = cv2.imread(image_path, cv2.IMREAD_COLOR)

#     # Pad the image for DCT processing
#     padded_img = pad_for_dct(img)
#     img_float = padded_img.astype(np.float32)

#     # Divide the image into 8x8 blocks
#     blocks = img_float.reshape((img_float.shape[0] // 8, img_float.shape[1] // 8, 8, 8, 3))

#     # Apply DCT to each block
#     dct_blocks = np.zeros_like(blocks)
#     for i in range(blocks.shape[0]):
#         for j in range(blocks.shape[1]):
#             for k in range(blocks.shape[2]):
#                 for l in range(blocks.shape[3]):
#                     for m in range(blocks.shape[4]):
#                         dct_blocks[i, j, k, l, m] = cv2.dct(blocks[i, j, k, l, m])

#     # Extract message bits from selected DCT coefficients
#     extracted_bits = []
#     for i in range(blocks.shape[0]):
#         for j in range(blocks.shape[1]):
#             for k in range(blocks.shape[2]):
#                 for l in range(blocks.shape[3]):
#                     for m in range(4):  # Extract from the first 4 coefficients in each block
#                         extracted_bits.append(str(int(dct_blocks[i, j, k, l, 0, m]) % 2))

#     # Combine extracted bits into a binary string
#     extracted_message = ''.join(extracted_bits)

#     # Convert binary string to ASCII text (assuming hexadecimal encoding)
#     try:
#         extracted_message = binascii.a2b_hex(extracted_message).decode('ascii')
#     except binascii.Error:
#         extracted_message = ""  # Handle invalid binary data

#     return extracted_message
#     """Decodes a message hidden in an image using DCT."""
#     img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
#     img_float = img.astype(np.float32)

#     blocks = img_float.reshape((img_float.shape[0] // 8, 8, img_float.shape[1] // 8, 8))
#     dct_blocks = np.zeros_like(blocks)

#     for i in range(blocks.shape[0]):
#         for j in range(blocks.shape[1]):
#             dct_blocks[i, j] = cv2.dct(blocks[i, j])

#     extracted_bits = []
#     for i in range(blocks.shape[0]):
#         for j in range(blocks.shape[1]):
#             for k in range(4):
#                 extracted_bits.append(str(int(dct_blocks[i, j, 0, k]) % 2))

#     extracted_message = ''.join(extracted_bits)
#     print("Extracted Binary Message:", extracted_message)

#     try:
#         extracted_message = binascii.a2b_hex(extracted_message).decode('ascii')
#     except binascii.Error:
#         extracted_message = ""

#     print("Extracted Message (text):", extracted_message)

#     return extracted_message
#     img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
#     img_float = img.astype(np.float32)

#     blocks = img_float.reshape((img_float.shape[0] // 8, 8, img_float.shape[1] // 8, 8))
#     dct_blocks = np.zeros_like(blocks)

#     for i in range(blocks.shape[0]):
#         for j in range(blocks.shape[1]):
#             dct_blocks[i, j] = cv2.dct(blocks[i, j])

#     extracted_bits = []

#     for i in range(blocks.shape[0]):
#         for j in range(blocks.shape[1]):
#             for k in range(4):
#                 extracted_bits.append(str(floor(dct_blocks[i, j, 0, k] % 2)))

#     print(extracted_bits)
#     extracted_message = ''.join(extracted_bits)

#     # Convert binary string to ASCII text (assuming hexadecimal encoding)
#     try:
#         extracted_message = binascii.a2b_hex(extracted_message).decode('ascii')
#     except binascii.Error:
#         extracted_message = ""  # Handle invalid binary data

#     return extracted_message

from PIL import Image
import numpy as np
from stegano import lsb

def embed_message(image_path, message, save_path):
    original_image = Image.open(image_path)
    encoded_image = lsb.hide(original_image, message)
    encoded_image.save(save_path, "PNG")

def extract_message(encoded_image_path):
    encoded_image = Image.open(encoded_image_path)
    message = lsb.reveal(encoded_image)
    return message

# # Example usage
# image_path = 'image.png'
# message = "Hello, this is a secret message!"
# embed_message(image_path, message)

path1 = "D:/Projects/steganography-git/media/encoded/DCT__03aaad2d-1bee-49eb-b89f-746631bfeb9f.png"
path3 = "D:/Projects/steganography-git/media/encoded/DCT__7248754f-9743-4c85-9353-dee44ae107c5.jpg"

# # Extract the message from the steganographed image
# extracted_message = extract_message(path1)
# print("Extracted message:", extracted_message)
