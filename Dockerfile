# Base image dengan Python 3.12
FROM python:3.12-slim

# Instalasi dependencies tambahan untuk menjalankan aplikasi GUI di container
RUN apt-get update && apt-get install -y \
    python3-tk \
    libx11-6 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements.txt dan install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua file ke dalam container
COPY . .

# Jalankan aplikasi
CMD ["python", "main.py"]
