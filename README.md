## SocketJoy

Use your mobile phone as a virtual xbox controller for your windows or linux pc!

This project relies on work done by @qbolec with [joydiv](https://github.com/qbolec/Joydiv) and the [j2dx](https://github.com/OzymandiasTheGreat/Joy2DroidX-server/) server written by @OzymandiasTheGreat, so huge thanks to them!

### Quickstart

#### Windows

__Server:__
```
wget https://github.com/OzymandiasTheGreat/Joy2DroidX-server/releases/download/v0.1.0/Joy2DroidX-server-0.1.0-x86_64.exe
```

Or simply download and run this server [executable](https://github.com/OzymandiasTheGreat/Joy2DroidX-server/releases/download/v0.1.0/Joy2DroidX-server-0.1.0-x86_64.exe)

Note that you can run the exe in a cmd terminal and pass in `-d` to enable debugging on the server side.
```
Joy2DroidX-server-0.1.0-x86_64.exe -d
```
(Note that the qr code and address output from this command is for the j2dx server which the client connects to. Incase the default server address in `socketjoy.js` is different from the one provided in the output, just update the address in `socketjoy.js` or manually enter the address on your smartphone by clicking the cog button)

__Client:__

```
git clone https://github.com/harsh2204/socketjoy.git
cd socketjoy
python3 -m http.server
```

Connect to the __client__ address with the correct port to complete the quickstart.

---

#### Linux:

The following script is a quick way to get the server and client up and running with one command. The server and client will be installed in a directory called `virtual-controller`. 
```
bash <(curl -s https://gist.githubusercontent.com/harsh2204/ad0edf5ef6298464fb5f6d50bd01196f/raw)
```

To run the server again you can simply go into `virtual-controller/socket-joy` and run `./run.sh`.

### Manual Setup and Deployment Steps:

* install j2dx plugin and set it up. See instuctions [from my fork](https://github.com/harsh2204/Joy2DroidX-server) or  [here](https://github.com/OzymandiasTheGreat/Joy2DroidX-server/#installation)
* edit socketjoy.js to open the socket at the local IP address of your machine on line. Alternatively, you can also do this in the browser after you connect you smartphone..
* run a j2dx instance by simply running `j2dx` or `j2dx -d` for debugging.
* run `python -m http.server 8080` to serve the virtual controller front-end.
* connect to your <local-ip-of-host>:8080 from your mobile device and start playing some games!

--- 

TODO: Reimplement the front end rendering to support custom positions and controller configurations in general!

### Implemenation Status:

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
