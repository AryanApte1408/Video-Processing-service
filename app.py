from flask import Flask, request, render_template, send_file
import mysql.connector
from moviepy.editor import VideoFileClip
import os

app = Flask(__name__)

# Configure MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="vidyo"
)

# Define the paths for uploads and audio files
UPLOADS_FOLDER = 'uploads/'
AUDIO_FOLDER = 'audio/'

# Ensure the folder structure exists
if not os.path.exists(UPLOADS_FOLDER):
    os.makedirs(UPLOADS_FOLDER)
if not os.path.exists(AUDIO_FOLDER):
    os.makedirs(AUDIO_FOLDER)

@app.route('/')
def hello_world():
    return 'Hello, World!'

# Define a route for the test form
@app.route('/audio_extract_test.html', methods=['GET'])
def test_audio_extraction():
    return render_template('audio_extract_test.html')

@app.route('/extract_audio', methods=['POST'])
def extract_audio():
    try:
        video_file = request.files['video']
        user = request.form['user']

        if video_file:
            # Save the uploaded video file
            video_path = os.path.join(UPLOADS_FOLDER, video_file.filename)
            video_file.save(video_path)

            # Extract audio
            video_clip = VideoFileClip(video_path)
            audio_clip = video_clip.audio
            audio_filename = video_file.filename.replace('.mp4', '.mp3')
            audio_path = os.path.join(AUDIO_FOLDER, audio_filename)
            audio_clip.write_audiofile(audio_path)

            # Store information in the database
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO videos (user, audio_file_path) VALUES (%s, %s)",
                (user, audio_path)
            )
            db.commit()
            cursor.close()

            # Return the extracted audio file for download
            return send_file(audio_path, as_attachment=True)
        else:
            return 'No video file provided', 400

    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
