import os
from scripts.player import Player
from scripts.AudioAnalyzer import AudioAnalyzer
from flask import Flask,render_template, url_for, flash, request, redirect
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './static/uploads'
LOG_FOLDER = './static/logs'
WAV_FOLDER = './static/wav_files'
SCRIPT_FOLDER = './scripts'
ALLOWED_EXTENSIONS = set(['wav'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['LOG_FOLDER'] = LOG_FOLDER
app.config['WAV_FOLDER'] = WAV_FOLDER
app.config['SCRIPT_FOLDER'] = SCRIPT_FOLDER
app.config['PLAYER'] = Player()
app.config['ANALYZER'] = AudioAnalyzer()

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
            return redirect(url_for('foleyizing', filename=filename))
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

    randomFile = app.config['PLAYER'].playRandom(pathToFillerDir=audioFillerDir)
    return render_template('player.html', random_audio=randomFile)

@app.route('/testAudioAnalyzer')
def testAudioAnalyzer():
    #Do foleyizing then redirect to finish page when complete, will show spectrogram and show foleyized audio player
    original = os.path.join(app.config['WAV_FOLDER'], 'badness.wav')
    mixed = app.config['ANALYZER'].findDeadAreas(altPath=original, outDir=app.config['WAV_FOLDER'])
    return render_template('analysis.html', original_audio=original, mixed_audio=mixed)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8181)
