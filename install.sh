#! /usr/bin/env bash

source ./bin/activate || { echo 'pyenv could not be activated, please ensure that this script exists in a pyenv project' ; exit 1; }
git clone https://github.com/harsh2204/Joy2DroidX-server.git j2dx-server/
git clone https://github.com/harsh2204/socketjoy.git socket-joy/

pip install -I j2dx-server/
sudo j2dx --setup
cd socket-joy/
./run.sh && deactivate
