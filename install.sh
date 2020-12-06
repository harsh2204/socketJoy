#! /usr/bin/env bash

mkdir j2dx-server
mkdir socket-joy

git clone https://github.com/harsh2204/Joy2DroidX-server.git j2dx-server/
git clone https://github.com/harsh2204/socketjoy.git socket-joy/

./socket-joy/run.sh
