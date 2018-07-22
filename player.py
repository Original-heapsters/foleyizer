import os
import wave
import random
import contextlib
import simpleaudio as sa
from pydub import AudioSegment as dub

class Player:
    def __init__(self, currentAudioPath=None):
        self.currentAudioPath = currentAudioPath
        return

    def playWav(self, pathToWav=None):
        if pathToWav is not None and pathToWav != '':
            wave_obj = sa.WaveObject.from_wave_file(pathToWav)
            play_obj = wave_obj.play()
            play_obj.wait_done()
        else:
            return 'No audio path provided'

    def playRandom(self, pathToFillerDir=None):
        if pathToFillerDir is not None and pathToFillerDir != '':
            files = []
            for file in os.listdir(pathToFillerDir):
                if file.endswith(".wav"):
                    path = os.path.join(pathToFillerDir, file)
                    files.append(path)
            selectedFile = random.choice(files)
            self.playWav(pathToWav=selectedFile)
            return selectedFile

    def combineAudioFiles(self, src=None, filler=None, offset=0):
        if src and filler:
            baseAudio = dub.from_wav(src)
            fillerAudio = dub.from_wav(filler)

            # mix sound2 with sound1, starting at 5000ms into sound1)
            output = baseAudio.overlay(fillerAudio, position=offset)

            # save the result
            destination = './wav_files/mixed_audio.wav'
            output.export(destination, format='wav')

            return destination

        else:
            return 0
            
    def getWavLength(self, pathToWav=None):
        with contextlib.closing(wave.open(pathToWav,'r')) as f:
           frames = f.getnframes()
           rate = f.getframerate()
           duration = frames / float(rate)
           
           return duration
           
        return 0


if __name__ == '__main__':
    import sys

    print ('Number of arguments:', len(sys.argv), 'arguments.')
    print ('Argument List:', str(sys.argv))
    if len(sys.argv) > 1 :
            print ("test")
            pathToTestFile = sys.argv[1]
            print (str(pathToTestFile))
            play = Player(currentAudioPath=None)
            play.playWav(pathToWav=pathToTestFile)

    else:
            print ("other test")
            pathToTestFile = './wav_files/test.wav'
            pathToFillers = './wav_files/filler/'
            play = Player(currentAudioPath=None)
            print('Playing test file')
            #play.playWav(pathToWav=pathToTestFile)
            print('Playing random filler file')
            selected = play.playRandom(pathToFillerDir=pathToFillers)
            print('Mixing audio')
            mixed = play.combineAudioFiles(src=pathToTestFile, filler=selected)
            print('Playing mixed audio')
            play.playWav(mixed)
            print('Mixed audio duration is ' + str(play.getWavLength(mixed)))
