# Use official Python image
FROM python:3.10.12

# Environment variables to improve Python behavior
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install necessary packages
RUN apt-get update && apt-get install -y \
    gettext \
    build-essential \
    wget \
    python3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Download and build TA-Lib from source
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz \
    && tar -xzf ta-lib-0.4.0-src.tar.gz \
    && cd ta-lib \
    && ./configure --prefix=/usr \
    && make \
    && make install \
    && rm -rf ta-lib ta-lib-0.4.0-src.tar.gz
# Upgrade pip and setuptools
RUN pip install --upgrade pip setuptools

# Set working directory
WORKDIR /django

# Copy requirements.txt and install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Make the necessary scripts executable
RUN chmod +x install_talib.sh entrypoint.sh 

# Run the script to install TA-Lib
RUN ./install_talib.sh

# Entrypoint for the container
ENTRYPOINT ["./entrypoint.sh"]
