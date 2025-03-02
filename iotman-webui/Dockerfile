# Use the latest Python 3.12 slim image for a lightweight build
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . /app

# Expose the port NiceGUI runs on (8080)
EXPOSE 3000

# No CMD instruction needed as it will be provided by Docker Compose


