# Use an official Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the application files
COPY expirarr/ ./expirarr/

# Copy the requirements file
COPY requirements.txt .

# Copy the config file
COPY config/config.example.yaml ./config/config.yaml
COPY config/config.example.yaml ./expirarr/config.example.yaml

# Copy the entrypoint script
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Copy the fonts folder
COPY fonts/ ./fonts/

# Install dependencies
RUN apt-get update && apt-get install -y \
    libfreetype6-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt 

# Set environment variable for unbuffered Python output
ENV PYTHONUNBUFFERED=1

# Command to run the script
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["python", "-u", "-m", "expirarr.main"]
