FROM python:3.7.4

RUN printf "deb http://archive.debian.org/debian/ jessie main\ndeb-src http://archive.debian.org/debian/ jessie main\ndeb http://security.debian.org jessie/updates main\ndeb-src http://security.debian.org jessie/updates main" > /etc/apt/sources.list
RUN apt update -y

WORKDIR /app
COPY requirements.txt .
RUN pip install -r /app/requirements.txt

CMD ["/bin/sh", "-c", "while true; do echo hello world; sleep 1; done"]
