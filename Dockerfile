FROM python:3.8-slim-buster

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

ADD . /aw
WORKDIR /aw

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY audio_wizard.py /

ENTRYPOINT ["python", "audio_wizard.py"]
