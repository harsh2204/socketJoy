## SocketJoy

**Note** : This project is currently only being tested on linux (and may not work on windows). Once the frontend implementation is done, I'll start testing on windows.

Use your mobile phone as a virtual xbox controller for your windows or linux pc!

This project relies on work done by @qbolec with [joydiv](https://github.com/qbolec/Joydiv) and the [j2dx](https://github.com/OzymandiasTheGreat/Joy2DroidX-server/) server written by @OzymandiasTheGreat, so huge thanks to them!


**NOTE**: This project is WIP, however as it stands right now you can serve the index.html, connect to it on your local network using your device and have the controller running with limited functionality as stated in the implementation status section. Run the j2dx server and add the local address to the CORS allowed list to get the virtual controller up and running.

### Steps to get this up and running:

* install j2dx plugin and set it up. See instuctions [from my fork](https://github.com/harsh2204/Joy2DroidX-server) or  [here](https://github.com/OzymandiasTheGreat/Joy2DroidX-server/#installation)
* edit socketjoy.js to open the socket at the local IP address of your machine on line.
* run a j2dx instance by simply running `j2dx` or `j2dx -d` for debugging.
* run `python -m http.server 8080` to serve the virtual controller front-end.
* connect to your <local-ip-of-host>:8080 from your mobile device and start playing some games!

--- 

### Implemenation Status

**Button/Command**|** Status**
:-----:|:-----:
main-button|✅
back-button|✅
start-button|✅
left-stick-press|❎
right-stick-press|❎
left-bumper|✅
left-trigger|❎
right-bumper|✅
right-trigger|❎
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
