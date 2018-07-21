import simpleaudio as sa

class Player:
    def __init__(self, currentAudioPath=None):
        self.currentAudioPath = currentAudioPath
        return

    def playWav(self, pathToWav=None):
        if pathToWav is not None or pathToWav != '':
            wave_obj = sa.WaveObject.from_wave_file(pathToWav)
            play_obj = wave_obj.play()
            play_obj.wait_done()
        else:
            return 'No audio path provided'

if __name__ == '__main__':
    pathToTestFile = 'wav_files/back2work.wav'
    play = Player(currentAudioPath=None)
    play.playWav(pathToWav=pathToTestFile)
