import os
from pydub import AudioSegment

def convert_mp3_to_wav(filepath,outputpath=None):
    sound = AudioSegment.from_mp3(filepath)
    new_path = filepath.split('.')[0]
    if outputpath==None: outputpath=new_path+'.wav'
    directory = reduce(lambda x,y: x+'/'+y, outputpath.split('/')[:-1])+'/'
    if not os.path.exists(directory): os.mkdir(directory)
    sound.export(outputpath, format="wav")
    return outputpath

def convert_flac_to_wav(filepath,outputpath=None):
    sound = AudioSegment.from_flac(filepath)
    new_path = filepath.split('.')[0]
    if outputpath==None: outputpath=new_path+'.wav'
    directory = reduce(lambda x,y: x+'/'+y, outputpath.split('/')[:-1])+'/'
    if not os.path.exists(directory): os.mkdir(directory)
    sound.export(outputpath, format="wav")
    return outputpath
