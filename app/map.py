
from app.algorithms import BPCAlgorithm as BPC, DCTAlgorithm as DCT, DFTAlgorithm as DFT, LSBAlgorithm as LSB, SpreadSpectrumAlgorithm as SS, AudioAlgorithm as Audio, VideoAlgorithm as Video

ALGO_MAP = {
    # png, jpg
    "BPC": {
        "encode": BPC.bpc_encode,# image_path, message, save_path -> save_path
        "decode": BPC.bpc_decode,# image_path  -> message
        "allowed": ["png", "jpg", "bmp", "tiff"]
    },
    # gif, png, jpg
    "LSB": {
        "encode": LSB.hide_message, # image_path, message, save_path -> save_path
        "decode": LSB.extract_message, # image_path -> message
        "allowed": ["png", "jpg", "bmp", "tiff"]
    },
    # png,
    "DCT": {
        "encode": DCT.DCT().encode_image, # image_path, message, save_path -> save_path
        "decode": DCT.DCT().decode_image, # image_path -> message
        "allowed": ["png"]
    },
    # png 
    "DFT": {
        "encode": DFT.hide_message, # image_path, message, save_path -> save_path
        "decode": DFT.reveal_message, # HIDDEN_image_path -> message,
        "allowed": ["png", "bmp", "tiff"]
    },
    # png, jpg, bmp, tiff
    "SS": {
        "encode": {
            "image": SS.embed_message, # image_path, message, save_path -> spreading_sequence
            "audio": Audio.hide_text_in_audio,# source_path, hidden_text target_path,
            "video": Video.encode, # file_path, secret_message, frame_save_path
        }, 
        "decode": {
            "image": SS.extract_message, # image_path, spreading_sequence, message_length -> message
            "audio": Audio.show_hidden_text_in_audio,# file_path  -> message
            "video": Video.decode, # frame_save_path  -> message
        },
        "allowed": ["png", "jpg", "bmp", "tiff", "mp4", "mp3"]
    }
}