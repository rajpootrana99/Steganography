
from app.algorithms import BPCAlgorithm as BPC, DCTAlgorithm as DCT, DFTAlgorithm as DFT, LSBAlgorithm as LSB, SpreadSpectrumAlgorithm as SS

ALGO_MAP = {
    # png, jpg
    "BPC": {
        "encode": BPC.bpc_encode,# image_path, message, save_path -> save_path
        "decode": BPC.bpc_decode,# image_path  -> message
        "allowed": ["png", "jpg"]
    },
    # gif, png, jpg
    "LSB": {
        "encode": LSB.hide_message, # image_path, message, save_path -> save_path
        "decode": LSB.extract_message, # image_path -> message
        "allowed": ["png", "jpg"]
    },
    # png, jpg
    "DCT": {
        "encode": DCT.embed_message, # image_path, message, save_path -> save_path
        "decode": DCT.extract_message, # image_path -> message
        "allowed": ["png", "jpg"]
    },
    # png 
    "DFT": {
        "encode": DFT.hide_message, # image_path, message, save_path -> save_path
        "decode": DFT.reveal_message, # HIDDEN_image_path -> message,
        "allowed": ["png"]
    },
    # png, jpg
    "SS": {
        "encode": SS.embed_message, # image_path, message, save_path -> spreading_sequence
        "decode": SS.extract_message, # image_path, spreading_sequence, message_length -> message
        "allowed": []
    }
}