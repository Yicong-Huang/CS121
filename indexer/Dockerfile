FROM ubuntu:bionic

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3.7 python-pip build-essential

WORKDIR /tmp
ADD http://download.redis.io/redis-stable.tar.gz .
RUN tar xzvf redis-stable.tar.gz && cd redis-stable && make -j8 && make install

VOLUME /app
WORKDIR /app

COPY src/requirements.txt .

RUN pip install --no-cache -r requirements.txt

COPY entry.sh /entry.sh
ENTRYPOINT [ "/entry.sh" ]
