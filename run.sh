#!/bin/sh
function usage() {
    echo "Usage: ./run.sh [virtual-env-directory]"
    echo
}
function error() {
    echo "Something went wrong when sourcing the venv. Please check your venv directory and ensure j2dx is installed correctly."
    usage
    exit 1
}

type -t j2dx >/dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "j2dx found! running instance"
else
    if [ "$#" -eq 1 ]; then
        source $1/bin/activate || error

        type -t j2dx >/dev/null 2>&1 || error
        
    elif [ "$#" -eq 0 ]; then
        echo "Sourcing default directory from ../bin/activate"
        source ../bin/activate
    else
        usage
        exit 1
    fi
fi

j2dx & python3 -m http.server && kill $!