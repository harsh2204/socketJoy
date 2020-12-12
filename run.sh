#! /usr/bin/env bash
which deactivate
rv=$?
if [ $rv -eq 0 ]; then
    echo "venv already sourced"
else
    source ../bin/activate
fi

j2dx & python3 -m http.server && kill $! && deactivate
