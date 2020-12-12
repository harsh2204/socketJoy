## SocketJoy

**Note** : This project is currently only being tested on linux (and may not work on windows). Once the frontend implementation is done, I'll start testing on windows.

Use your mobile phone as a virtual xbox controller for your windows or linux pc!

This project relies on work done by @qbolec with [joydiv](https://github.com/qbolec/Joydiv) and the [j2dx](https://github.com/OzymandiasTheGreat/Joy2DroidX-server/) server written by @OzymandiasTheGreat, so huge thanks to them!

### Install Script:
The following script is a quick way to get the server and client up and running with one(sort-of) command.
```
python3 -m venv virtual-controller && cd virtual-controller; bash <(curl -s https://raw.githubusercontent.com/harsh2204/socketjoy/master/install.sh)
```

### Steps to get this up and running:

* install j2dx plugin and set it up. See instuctions [from my fork](https://github.com/harsh2204/Joy2DroidX-server) or  [here](https://github.com/OzymandiasTheGreat/Joy2DroidX-server/#installation)
* edit socketjoy.js to open the socket at the local IP address of your machine on line. Alternatively, you can also do this in the browser after you connect you smartphone..
* run a j2dx instance by simply running `j2dx` or `j2dx -d` for debugging.
* run `python -m http.server 8080` to serve the virtual controller front-end.
* connect to your <local-ip-of-host>:8080 from your mobile device and start playing some games!

--- 

TODO: Reimplement the front end rendering to support custom positions and controller configurations in general!

### Implemenation Status

**Button/Command**|** Status**
:-----:|:-----:
main-button|✅
back-button|✅
start-button|✅
left-stick-press|❎
right-stick-press|❎
left-bumper|✅
left-trigger|✅
right-bumper|✅
right-trigger|✅
up-button|✅
right-button|✅
down-button|✅
left-button|✅
y-button|✅
x-button|✅
a-button|✅
b-button|✅
left-stick|✅
right-stick|✅
