FROM python:3.10.12
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y gettext

RUN pip install --upgrade pip


WORKDIR /django

# Copy the installation script to the image
COPY install_talib.sh install_talib.sh

RUN chmod +x install_talib.sh

# Install the TA-Lib C library before installing any package requirements
# Else, the TA-Lib Python wrapper package will fail to install
RUN ./install_talib.sh -p 3.10.12 -e ./talib_test_env

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]


