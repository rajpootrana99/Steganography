from PIL import Image
# pip install pillow

def message_to_binary(message):
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    return binary_message

def binary_to_message(binary_message):
    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        message += chr(int(byte, 2))
    return message


def hide_message(image_path, message, save_path):
    img = Image.open(image_path)

    # Convert the image to RGBA format if it's not already
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    # Convert the message to binary
    binary_message = message_to_binary(message)

    # Check if the message can fit in the image
    if len(binary_message) > img.width * img.height * 3:
        raise ValueError("Message too long to hide in the image")

    # Add termination signal to the binary message
    binary_message += '1111111111111110'

    data_index = 0
    for y in range(img.height):
        for x in range(img.width):
            pixel = list(img.getpixel((x, y)))
            for i in range(3):
                if data_index < len(binary_message):
                    pixel[i] = pixel[i] & ~1 | int(binary_message[data_index])
                    data_index += 1
            img.putpixel((x, y), tuple(pixel))

    # Convert the image to RGB before saving as JPEG
    
    # img = img.convert("RGB")
    
    # Save the image as PNG
    img.save(save_path, "PNG")
    
    print("Message hidden successfully.")

    return save_path

def extract_message(image_path):
    img = Image.open(image_path)

    # Convert to RGBA only if the image is not already in that mode
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    binary_message = ''

    for y in range(img.height):
        for x in range(img.width):
            pixel = img.getpixel((x, y))
            for i in range(3):
                binary_message += str(pixel[i] & 1)

    # Print debug information
    # print("Binary Message:", binary_message)

    end_index = binary_message.find('1111111111111110')
    print("Termination Signal Index:", end_index)

    binary_message = binary_message[:end_index]

    message = binary_to_message(binary_message)
    return message

# def hide_message(image_path, message, save_path):
#     img = Image.open(image_path)
#     img_format = img.format
#     if img_format != "PNG" or img_format != "png":
#         img = img.convert("RGBA")
#     binary_message = message_to_binary(message)

#     if len(binary_message) > img.width * img.height * 3:
#         raise ValueError("Message too long to hide in the image")

#     binary_message += '1111111111111110'  # Adding termination signal

#     data_index = 0
#     for y in range(img.height):
#         for x in range(img.width):
#             pixel = list(img.getpixel((x, y)))
#             for i in range(3):
#                 if data_index < len(binary_message):
#                     pixel[i] = pixel[i] & ~1 | int(binary_message[data_index])
#                     data_index += 1
#             img.putpixel((x, y), tuple(pixel))


#     if img_format != "PNG" or img_format != "png":
#         img= img.convert("RGB")
        
#     img.save(save_path)
    
#     print("Message hidden successfully.")
    
#     return save_path

# def extract_message(image_path):
#     img = Image.open(image_path)
#     img_format = img.format
    
#     if img_format != "PNG" or img_format != "png":
#         img = img.convert("RGBA")
        
#     binary_message = ''

#     for y in range(img.height):
#         for x in range(img.width):
#             pixel = img.getpixel((x, y))
#             for i in range(3):
#                 binary_message += str(pixel[i] & 1)

#     end_index = binary_message.find('1111111111111110')
#     binary_message = binary_message[:end_index]

#     message = binary_to_message(binary_message)
#     return message

# # Example usage
# message_to_hide = "Hello, this is a secret message!"
# hide_message("original_image.png", message_to_hide)


path1 = "D:/Projects/steganography-git/media/encoded/LSB__e021e8af-3848-4fa8-a53c-89be6946869f.png"
path3 = "D:/Projects/steganography-git/media/encoded/LSB__9699ce51-f1ad-47b1-be89-3e9c29a68dd4.jpg"

# extracted_message = extract_message(path1)
# print("Extracted message:", extracted_message)
