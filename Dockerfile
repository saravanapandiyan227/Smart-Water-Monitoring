# Smart Water Monitoring - Docker Image
# Base image: python:3.11-slim (lightweight, no unnecessary packages)
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project source files into the image
COPY . .

# Create the /app/data directory (Docker Volume will be mounted here)
# This ensures the directory exists even if no volume is mounted
RUN mkdir -p /app/data

# Expose Flask application port
EXPOSE 5000

# Environment variables with safe defaults for the container
# Override DATABASE_PATH, ADMIN_PASSWORD, FLASK_SECRET_KEY at runtime
ENV FLASK_APP=app.py
ENV FLASK_DEBUG=false
ENV DATABASE_PATH=/app/data/water_monitoring.db
ENV ADMIN_USERNAME=admin
ENV ADMIN_PASSWORD=admin123
ENV FLASK_SECRET_KEY=change-this-in-production

# Start the Flask application
CMD ["python", "app.py"]
