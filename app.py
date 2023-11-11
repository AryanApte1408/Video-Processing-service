from flask import Flask, request, render_template, send_file, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from moviepy.editor import VideoFileClip, TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
import os

app = Flask(__name__)

# Configure SQLAlchemy
# Use 'host.docker.internal' as the host to connect to the MySQL server on the host machine
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@localhost/vidyo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the paths for uploads, audio files, and watermarks
UPLOADS_FOLDER = 'uploads/'
AUDIO_FOLDER = 'audio/'

# Ensure the folder structure exists
os.makedirs(UPLOADS_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# Define SQLAlchemy models
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50))
    audio_file_path = db.Column(db.String(255))

class Watermarking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_file_path = db.Column(db.String(255))
    watermark_type = db.Column(db.String(50))

def display_table_info(table):
    try:
        rows = table.query.all()
        columns = table.__table__.columns.keys()
        print(f"\nTable: {table.__tablename__}")
        print(columns)
        for row in rows:
            print(row)
    except Exception as e:
        print(f"Error in display_table_info: {str(e)}")

# Create the database tables before the first request is processed
def create_tables():
    with app.app_context():
        db.create_all()

# Check if the database tables need to be created before the first request
if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    create_tables()

@app.route('/')
def hello_world():
    return 'Welcome to my assignment application'

# Define a route for the test form
@app.route('/functionality.html', methods=['GET'])
def test_functionality():
    # Display information for 'videos' table
    display_table_info(Video)
    # Display information for 'watermarking' table
    display_table_info(Watermarking)
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
            new_video = Video(user=user, audio_file_path=audio_path)
            db.session.add(new_video)
            db.session.commit()

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
            new_watermarking = Watermarking(video_file_path=video_path, watermark_type="text")
            db.session.add(new_watermarking)
            db.session.commit()

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
    # Run the app with host set to '0.0.0.0' to make it externally accessible
    app.run(debug=True, host='0.0.0.0')
