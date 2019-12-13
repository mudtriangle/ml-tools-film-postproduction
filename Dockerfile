FROM ubuntu:18.04

RUN apt -y update
RUN apt-get -y update
RUN apt-get -y upgrade

RUN apt install -y git && apt-get install -y make && apt-get install -y pkg-config

RUN apt-get -y install ffmpeg
RUN apt-get install -y libsm6 libxext6 libxrender-dev

RUN apt-get install -y libltc-dev
RUN apt-get install -y libjack-dev
RUN apt-get install -y libsndfile-dev

RUN git clone https://github.com/x42/ltc-tools.git
RUN cd ltc-tools && make all && make install && cd .. && rm -r ltc-tools


RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r /app/requirements.txt

CMD ["/bin/sh", "-c", "while true; do echo hello world; sleep 1; done"]
