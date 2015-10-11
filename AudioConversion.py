from pydub import AudioSegment

def convert_mp3_to_wav(filepath):
    sound = AudioSegment.from_mp3(filepath)
    new_path = filepath.split('.')[0]
    sound.export(new_path+'.wav', format="wav")
    return new_path
