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
    libta-lib0 \
    libta-lib0-dev \
    python3-dev

# Upgrade pip
RUN pip install --upgrade pip



WORKDIR /django


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]