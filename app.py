from flask import Flask, request, render_template, send_file, redirect, url_for
import mysql.connector
from moviepy.editor import VideoFileClip, TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
import os

app = Flask(__name__)

# Configure MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="vidyo"
)

# Define the paths for uploads, audio files, and watermarks
UPLOADS_FOLDER = 'uploads/'
AUDIO_FOLDER = 'audio/'

# Ensure the folder structure exists
if not os.path.exists(UPLOADS_FOLDER):
    os.makedirs(UPLOADS_FOLDER)
if not os.path.exists(AUDIO_FOLDER):
    os.makedirs(AUDIO_FOLDER)

# Display table information function
def display_table_info(table_name):
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    print(f"\nTable: {table_name}")
    print(columns)
    for row in rows:
        print(row)
    cursor.close()

@app.route('/')
def hello_world():
    return 'Hello, World!'

# Define a route for the test form
@app.route('/functionality.html', methods=['GET'])
def test_functionality():
    # Display information for 'videos' table
    display_table_info('videos')
    # Display information for 'watermarking' table
    display_table_info('watermarking')
    return render_template('functionality.html')

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

@app.route('/watermark_video', methods=['POST'])
def watermark_video():
    try:
        video_file = request.files['video']

        if video_file:
            # Save the uploaded video file
            video_path = os.path.join(UPLOADS_FOLDER, video_file.filename)
            video_file.save(video_path)

            # Create a text watermark
            txt_clip = TextClip("Aryan.AI", fontsize=60, color='white')
            txt_clip = txt_clip.set_position(('right', 'bottom'))

            # Load the video clip
            video_clip = VideoFileClip(video_path)

            # Overlay the watermark on the video for the entire duration
            watermarked_video = CompositeVideoClip([video_clip, txt_clip.set_duration(video_clip.duration)])

            # Save the watermarked video
            watermarked_video_path = os.path.join(UPLOADS_FOLDER, 'watermarked_' + video_file.filename)
            watermarked_video.write_videofile(watermarked_video_path, codec="libx264")  # Specify the codec

            # Store information in the database
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO watermarking (video_file_path, watermark_type) VALUES (%s, %s)",
                (video_path, "text")
            )
            db.commit()
            cursor.close()

            return redirect(url_for('download', filename='watermarked_' + video_file.filename))

        else:
            return 'No video file provided', 400

    except Exception as e:
        return str(e), 500

# Define a route for downloading watermarked videos
@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    return send_file(os.path.join(UPLOADS_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
