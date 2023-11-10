# Use the official Python image as a base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Install the MySQL client library
RUN apt-get update && apt-get install -y default-libmysqlclient-dev

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Update pip and install required packages
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --default-timeout=100 -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Expose the port that your Flask app will run on
EXPOSE 8080

# Set the environment variable for Flask
ENV FLASK_APP=app.py

# Specify the command to run on container start
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8080"]
