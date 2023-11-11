# Video Processing Flask Application
## RUN THIS FILE-
app.py
## Prerequisites

Before running the Python-Flask application, ensure the following prerequisites are met on your system:

1. **FFmpeg:**
   - Install FFmpeg on your system. FFmpeg is used for video processing.
   - Visit the [FFmpeg official website](https://ffmpeg.org/download.html) for installation instructions.

2. **MySQL:**
   - Install MySQL on your system. The application uses MySQL as the database.
   - Visit the [MySQL official website](https://dev.mysql.com/downloads/mysql/) for installation instructions.

3. **ImageMagick:**
   - Install ImageMagick on your system. ImageMagick is used for image processing.
   - Visit the [ImageMagick official website](https://imagemagick.org/script/download.php) for installation instructions.

4. **Python Libraries:**
   - The following Python libraries are required. Install them using the provided command:

     ```bash
     pip install Flask Flask-SQLAlchemy moviepy mysql-connector-python
     ```

   - Additionally, install `Werkzeug` for secure filename handling:

     ```bash
     pip install Werkzeug
     ```

## Running the Application

1. **Database Configuration:**
   - Open `app.py` and update the database configuration:
     ```python
     app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@localhost/vidyo'
     ```

2. **Folder Structure:**
   - Ensure the existence of the required folders:
     ```bash
     mkdir uploads audio
     ```

3. **Create Database Tables:**
   - Run the application to create the necessary database tables:
     ```bash
     python app.py
     ```

4. **Running the Application:**
   - After configuring and creating the tables, you can access the application at `http://localhost:5000/functionality.html` in your web browser.

5. **Application Functionality:**
   - The Flask application provides the following functionalities:
     - **Audio Extraction:** Upload a video file, and the application extracts and provides the audio file for download.
     - **Video Watermarking:** Upload a video file, and the application adds a text watermark ("Aryan.AI") to the video, providing the watermarked video for download.

6. **Docker Usage:**
   - If you prefer to run the application using Docker, ensure Docker and Docker Compose are installed on your system.

   - Build the Docker image:
     ```bash
     docker-compose build
     ```

   - Run the Docker container:
     ```bash
     docker-compose up
     ```

## Docker Configuration Files

1. **Dockerfile:**
   - The `Dockerfile` contains instructions to build the Docker image. Ensure it is present in the project directory.

     ```dockerfile
     FROM python:3.8

     WORKDIR /app

     COPY . .

     RUN pip install -r requirements.txt

     CMD ["python", "app.py"]
     ```

2. **Docker Compose Configuration:**
   - The `docker-compose.yml` file defines the services, volumes, and dependencies for running the application in Docker.

     ```yaml
     version: '3'
     services:
       web:
         build: .
         ports:
           - "5000:5000"
         volumes:
           - .:/app
     ```

3. **Requirements File:**
   - The `requirements.txt` file lists the Python libraries required by the application.

     ```
     Flask
     Flask-SQLAlchemy
     moviepy
     mysql-connector-python
     Werkzeug
     ```

This documentation provides the necessary steps to set up and run the Flask application for video processing. Ensure you have the required dependencies installed, configure the database, and follow the specified steps to run the application either locally or using Docker. The application offers audio extraction and video watermarking functionalities.
