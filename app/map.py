
from app.algorithms import BPCAlgorithm as BPC, DCTAlgorithm as DCT, DFTAlgorithm as DFT, LSBAlgorithm as LSB, SpreadSpectrumAlgorithm as SS

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
        "encode": SS.embed_message, # image_path, message, save_path -> spreading_sequence
        "decode": SS.extract_message, # image_path, spreading_sequence, message_length -> message
        "allowed": ["png", "jpg", "bmp", "tiff"]
    }
}