FROM python:3.10.12
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y gettext

RUN pip install --upgrade pip


WORKDIR /django

RUN chmod +x install_talib.sh entrypoint.sh

RUN ./install_talib_nosudo.sh -p 3.10.12 -e ./talib_test_env

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

ENTRYPOINT ["./entrypoint.sh"]


