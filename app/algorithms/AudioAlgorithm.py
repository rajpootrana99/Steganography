from mutagen.id3 import ID3, TIT2, COMM, ID3NoHeaderError
from mutagen.mp3 import MP3
import shutil

# pip install mutagen

def hide_text_in_audio(source_path, hidden_text, target_path):
    try:
        shutil.copy2(source_path, target_path)
        
        # Attempt to load ID3 tag from the copied file, or create one if it doesn't exist
        try:
            audio = MP3(target_path, ID3=ID3)
        except ID3NoHeaderError:
            print("No ID3 tag found. Adding one.")
            audio = MP3(target_path)
            audio.add_tags()
        
        # Update or add the hidden text in the 'COMM' frame
        audio.tags.add(COMM(encoding=3, lang='eng', desc='hidden', text=hidden_text))

        # Save the modifications back to the file
        audio.save()
    except:
        return False
    return True

def show_hidden_text_in_audio(file_path):
    try:
        audio = MP3(file_path, ID3=ID3)
        
        # Assuming the text was hidden in the 'COMM' frame
        for key in audio.tags.keys():
            if key.startswith('COMM'):
                comm = audio.tags.get(key)
                # print(f"Hidden Text: {comm.text[0]}")
                return comm.text[0]
    
    except:
        return 'No Data Found'


# source_audio_path = 'mp3.mp3'
# target_audio_path = 'MP3_HIDDEN.mp3'
# text_to_hide = "It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like)."
# hide_text_in_audio(source_audio_path, target_audio_path, text_to_hide)

# hid_aud = show_hidden_text_in_audio(target_audio_path)

# print(hid_aud)