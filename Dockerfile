FROM python:3.8-slim-buster

WORKDIR /app

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y
RUN apt-get install -y fontforge potrace git
RUN apt-get install -y libjpeg-dev libtiff5-dev libpng-dev libfreetype6-dev libgif-dev libgtk-3-dev libxml2-dev libpango1.0-dev libcairo2-dev libspiro-dev libuninameslist-dev python3-dev ninja-build cmake build-essential gettext
RUN git clone --depth 1 https://github.com/fontforge/fontforge
RUN cd fontforge
RUN mkdir build && cd build
RUN cmake -GNinja -ENABLE_PYTHON_SCRIPTING=ON -ENABLE_PYTHON_EXTENSION=ON ..
RUN ninja && ninja install
RUN cd ../..
RUN cp /usr/local/lib/python3/dist-packages/* /usr/lib/python3/dist-packages
RUN git clone --depth 1 https://github.com/cod-ed/handwrite server
RUN cd handwrite && pip install -e .
RUN cd ..

COPY default.json default.json
COPY . .

ENTRYPOINT ["python3"]
CMD ["app.py"]