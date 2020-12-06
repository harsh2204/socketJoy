#! /usr/bin/env bash

git clone https://github.com/harsh2204/Joy2DroidX-server.git j2dx-server/
git clone https://github.com/harsh2204/socketjoy.git socket-joy/

./bin/activate

pip install -I j2dx-server/
sudo j2dx --setup
cd socket-joy/
./run.sh && deactivate