FROM python:3.8-slim-buster

WORKDIR /app

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get install -y wget
RUN wget -O fontforge https://github.com/fontforge/fontforge/releases/download/20201107/FontForge-2020-11-07-21ad4a1-x86_64.AppImage
RUN chmod +x fontforge
RUN mv fontforge /usr/bin/
RUN apt-get install -y potrace
ENV APPIMAGE_EXTRACT_AND_RUN=1


COPY requirements.txt requirements.txt
COPY default.json default.json
RUN pip3 install -r requirements.txt

COPY . .


CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]