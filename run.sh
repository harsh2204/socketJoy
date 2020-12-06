#! /usr/bin/env bash
python3 ../j2dx-server/j2dx/__init__.py & python3 -m http.server && kill $!
