import os
from scripts.player import Player
from scripts.AudioAnalyzer import AudioAnalyzer
from scripts.spectrogram import Spectrogram
from flask import Flask,render_template, url_for, flash, request, redirect
from werkzeug.utils import secure_filename

STATIC_FOLDER = './static'
UPLOAD_FOLDER = './static/uploads'
LOG_FOLDER = './static/logs'
WAV_FOLDER = './static/wav_files'
SCRIPT_FOLDER = './scripts'
ALLOWED_EXTENSIONS = set(['wav'])

app = Flask(__name__)
app.config['STATIC_FOLDER'] = STATIC_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['LOG_FOLDER'] = LOG_FOLDER
app.config['WAV_FOLDER'] = WAV_FOLDER
app.config['SCRIPT_FOLDER'] = SCRIPT_FOLDER
app.config['PLAYER'] = Player()
app.config['ANALYZER'] = AudioAnalyzer()
app.config['SPECTROGRAM'] = Spectrogram()

os.system('mkdir -p ' + app.config['LOG_FOLDER'])
os.system('mkdir -p ' + app.config['UPLOAD_FOLDER'])

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('doTheWholeShebang', filename=filename))
        return render_template('upload.html')
    else:
        return render_template('upload.html')

@app.route('/foleyizing')
def foleyizing():
    if request.args.get('filename',None):
        #Do foleyizing then redirect to finish page when complete, will show spectrogram and show foleyized audio player
        audioFile = os.path.join(app.config['UPLOAD_FOLDER'], request.args.get('filename', None))
        app.config['PLAYER'].playWav(audioFile)
    return render_template('loading.html')

@app.route('/testPlayer')
def testPlayer():
    #Do foleyizing then redirect to finish page when complete, will show spectrogram and show foleyized audio player
    audioFillerDir = os.path.join(app.config['WAV_FOLDER'], 'filler')

    randomFile = app.config['PLAYER'].playRandom(pathToFillerDir=audioFillerDir, shouldPlay=False)
    allFillers = app.config['PLAYER'].getListOfFillers(pathToFillerDir=audioFillerDir)
    return render_template('player.html', random_audio=randomFile, fillerFiles=allFillers)

@app.route('/testAudioAnalyzer')
def testAudioAnalyzer():
    #Do foleyizing then redirect to finish page when complete, will show spectrogram and show foleyized audio player
    original = os.path.join(app.config['WAV_FOLDER'], 'badness.wav')
    mixed, original_audio = app.config['ANALYZER'].findDeadAreas(altPath=original, outDir=app.config['WAV_FOLDER'])
    return render_template('analysis.html', original_audio=original_audio, mixed_audio=mixed)

@app.route('/testSpectrogram')
def testSpectrogram():
    #Do foleyizing then redirect to finish page when complete, will show spectrogram and show foleyized audio player
    pathToWav = os.path.join(app.config['WAV_FOLDER'], 'badness.wav')
    wav = app.config['SPECTROGRAM'].chooseWav(pathToWav)
    sound, graph, points = app.config['SPECTROGRAM'].graphSetting(wav)
    dura = app.config['SPECTROGRAM'].fileDuration(sound, graph)
    chan = app.config['SPECTROGRAM'].soundChannel(sound)
    plotTime = app.config['SPECTROGRAM'].plotTime(points,graph, chan)
    plotOutput = os.path.join(app.config['STATIC_FOLDER'], 'plot.png')
    spectrumPlot, json = app.config['SPECTROGRAM'].plotTone(plotTime, chan, outFile=plotOutput, showPlot=True, testAudio=pathToWav)
    return render_template('spectrogram.html', spectrum=spectrumPlot, timing=json)

@app.route('/doTheWholeShebang')
def doTheWholeShebang():
    if request.args.get('filename', None):
        #Do foleyizing then redirect to finish page when complete, will show spectrogram and show foleyized audio player
        pathToWav = os.path.join(app.config['UPLOAD_FOLDER'], request.args.get('filename', None))
        wav = app.config['SPECTROGRAM'].chooseWav(pathToWav)
        sound, graph, points = app.config['SPECTROGRAM'].graphSetting(wav)
        dura = app.config['SPECTROGRAM'].fileDuration(sound, graph)
        chan = app.config['SPECTROGRAM'].soundChannel(sound)
        plotTime = app.config['SPECTROGRAM'].plotTime(points,graph, chan)
        plotOutput = os.path.join(app.config['STATIC_FOLDER'], 'plot.png')
        spectrumPlot, json = app.config['SPECTROGRAM'].plotTone(plotTime, chan, outFile=plotOutput, showPlot=False, testAudio=pathToWav)

        mixedAudio, originalAudio = app.config['ANALYZER'].findDeadAreas(inputJson=json, outDir=app.config['WAV_FOLDER'])



        wav = app.config['SPECTROGRAM'].chooseWav(mixedAudio)
        sound, graph, points = app.config['SPECTROGRAM'].graphSetting(wav)
        dura = app.config['SPECTROGRAM'].fileDuration(sound, graph)
        chan = app.config['SPECTROGRAM'].soundChannel(sound)
        plotTime = app.config['SPECTROGRAM'].plotTime(points,graph, chan)
        plotOutput = os.path.join(app.config['STATIC_FOLDER'], 'mixplot.png')
        mixPlot, json = app.config['SPECTROGRAM'].plotTone(plotTime, chan, outFile=plotOutput, showPlot=False, testAudio=mixedAudio)


        print('mix at ' + mixedAudio + ' original at ' + originalAudio)
        return render_template('enchilada.html', original_audio=originalAudio, mixed_audio=mixedAudio, spectrum=spectrumPlot, mixedPlot=mixPlot, timing=json)
    else:
        return 'No filename Param'

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8181)
