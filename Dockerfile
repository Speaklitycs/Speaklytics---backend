# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Instal OpenCV prerequisites
RUN apt-get update && \
    apt-get install -y ffmpeg libsm6 libxext6 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Migrate
RUN python manage.py migrate

# Expose the port the app runs on
EXPOSE 8080

# Run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
