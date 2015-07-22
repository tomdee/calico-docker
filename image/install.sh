#!/usr/bin/env sh
apk update
apk add python
apk add --virtual build-dependencies python-dev build-base curl bash py-pip alpine-sdk libffi-dev openssl-dev
pip install -r /pycalico/requirements.txt

# Install Confd
curl -L https://www.github.com/kelseyhightower/confd/releases/download/v0.9.0/confd-0.9.0-linux-amd64 -o confd
chmod +x confd

pip install git+https://github.com/Metaswitch/python-etcd.git
pip install git+https://github.com/tomdee/calico.git

# BIRD