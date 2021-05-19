#!/bin/bash

apt-get install -y python3-pip
python3 -m pip install --trusted-host pypi.python.org -r requirements.txt
