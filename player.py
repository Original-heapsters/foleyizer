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
            fillers = self.getListOfFillers()
            selectedFile = random.choice(fillers)
            self.playWav(pathToWav=selectedFile)
            return selectedFile

    def getListOfFillers(self, pathToFillerDir=None):
        if pathToFillerDir is not None and pathToFillerDir != '':
            files = []
            for file in os.listdir(pathToFillerDir):
                if file.endswith(".wav"):
                    path = os.path.join(pathToFillerDir, file)
                    files.append(path)
            return files

    def combineAudioFiles(self, src=None, fillersWithOffsets=[]):
        if src and fillersWithOffsets:
            baseAudio = dub.from_mp3(src)
            intermediateAudio = None
            for filler, offset in fillersWithOffsets:
                fillerAudio = dub.from_mp3(filler)
                if not intermediateAudio:
                    intermediateAudio = baseAudio.overlay(fillerAudio, position=offset * 1000)
                else:
                    intermediateAudio = intermediateAudio.overlay(fillerAudio, position=offset * 1000)

            # save the result
            destination = './wav_files/mixed_audio.wav'
            if os.path.exists(destination):
                os.remove(destination)
            intermediateAudio.export(destination, format='wav')

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
