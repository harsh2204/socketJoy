#!/bin/bash

cd /home/pi/socketjoy

python3 server.py > sj.out 2>&1 #-d

exit 0
