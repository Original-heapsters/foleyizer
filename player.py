import os
import random
import simpleaudio as sa

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
            self.playWav(pathToWav=random.choice(files))


if __name__ == '__main__':
    pathToTestFile = './wav_files/test.wav'
    pathToFillers = './wav_files/filler/'
    play = Player(currentAudioPath=None)
    print('Playing test file')
    play.playWav(pathToWav=pathToTestFile)
    print('Playing random filler file')
    play.playRandom(pathToFillerDir=pathToFillers)
