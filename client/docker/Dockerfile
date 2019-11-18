FROM alpine

RUN apk add gcc musl-dev
RUN apk add python3-dev
RUN apk add --update \
    python \
    python-dev \
    py-pip \
    build-base \
  && pip install pycrypto
RUN apk add curl

COPY ./run.sh /run.sh
COPY ./Encryption.py /Encryption.py

