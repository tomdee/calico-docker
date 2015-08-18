FROM gliderlabs/alpine:latest

WORKDIR /code/

RUN apk update
RUN apk add bash

RUN apk add python-dev py-pip alpine-sdk
ADD requirements.txt /code/
RUN pip install --upgrade pip
RUN apk add libffi-dev openssl-dev
RUN pip install -r requirements.txt

ADD . /code/
ENTRYPOINT ["/code/calicoctl.py"]
CMD ["--help"]