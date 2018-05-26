FROM ubuntu:bionic

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3 python3-pip build-essential

WORKDIR /tmp
ADD http://download.redis.io/redis-stable.tar.gz .
RUN tar xzvf redis-stable.tar.gz && cd redis-stable && make -j8 && make install

VOLUME /app
WORKDIR /app

COPY src/requirements.txt .

RUN pip3 install --no-cache -r requirements.txt

VOLUME /redis-dump
COPY redis/ /redis
COPY entry.sh /entry.sh
ENTRYPOINT [ "/entry.sh" ]
