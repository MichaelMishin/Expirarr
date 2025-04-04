# Use an official Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the application files
COPY expirarr/ ./expirarr/

# Copy the requirements file
COPY requirements.txt .

# Copy the config file
COPY config.yaml ./config/config.yaml

# Install dependencies
RUN apt-get update && apt-get install -y \
    libfreetype6-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt 

# Command to run the script
CMD ["python", "-m", "expirarr.main"]
