FROM python:3.10.12
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y gettext

RUN pip install --upgrade pip



WORKDIR /django


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]