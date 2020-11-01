var SERVER_IP = "192.168.2.92:8013";// Change your ip here
function isLocalNetwork(hostname = window.location.hostname) {
  return (
    (['localhost', '127.0.0.1', '', '::1'].includes(hostname))
    || (hostname.startsWith('192.168.'))
    || (hostname.startsWith('10.0.'))
    || (hostname.endsWith('.local'))
  )
}

var isLocal = isLocalNetwork();
// var isLocal = false;

var sock;

if (isLocal) {
  sock = io(SERVER_IP);
} else {
  // Notify user that this is a demo only
  var demo = document.getElementById('demo');
  demo.style.display = 'block'
}

var conf = document.getElementsByClassName('configure')

function updateIP() {
  var ip = prompt('Please enter the j2dx server IP')
  console.log(ip)
  if (ip !== null) {
    SERVER_IP = ip;
    sock.close();
    sock = io(SERVER_IP);
  }
}

function send_input(key, value) {
  sock.emit("input", { key: key, value: value });
}
function createButton(id) {
  var button = document.getElementById(id);
  button.addEventListener(
    "touchstart",
    function (e) {
      send_input(id, 1);
      e.preventDefault();
    },
    false
  );
  button.addEventListener(
    "touchend",
    function (e) {
      send_input(id, 0);
      e.preventDefault();
    },
    false
  );
}
// Buttons
createButton("y-button");
createButton("x-button");
createButton("a-button");
createButton("b-button");

createButton("main-button");
createButton("back-button");
createButton("start-button");

createButton("left-bumper");
createButton("right-bumper");
// DPAD
// Use JoyDiv with 8 direction input, and emit them accordingly. So instead of sending the x and y values, send button 0 or 1
var dpad = document.getElementById("dpad");
var dpadjdiv = new JoydivModule.Joydiv({ element: dpad });
var dpad_down = {
  up: 0,
  down: 0,
  left: 0,
  right: 0,
};
dpad.addEventListener("joydiv-changed", function (e) {
  var input = dpadjdiv.getOneOf8Directions();
  var dname = input.name;
  if (dname !== "none") {
    var dirs = dname.split("-");
    for (const [key, value] of Object.entries(dpad_down)) {
      if (dirs.includes(key)) {
        send_input(key + "-button", 1);
        dpad_down[key] = 1;
      } else if (value == 1) {
        send_input(key + "-button", 0);
        dpad_down[key] = 0;
      }
    }
  }
});
// DPAD Reset
dpad.addEventListener("touchend", function (e) {
  for (var key in dpad_down) {
    dpad_down[key] = 0;
    send_input(key + "-button", 0);
  }
});

// Joysticks
var j1 = document.getElementById("joystick1");
var j2 = document.getElementById("joystick2");
var joydiv1 = new JoydivModule.Joydiv({
  element: j1,
  clampX: 1,
  clampY: 1,
  flipY: true,
});
var joydiv2 = new JoydivModule.Joydiv({
  element: j2,
  clampX: 1,
  clampY: 1,
  flipY: true,
});
j1.addEventListener("joydiv-changed", function (e) {
  var offset = joydiv1.getOneDirection().offset;
  sock.emit("input", { key: "left-stick-X", value: offset.x });
  sock.emit("input", { key: "left-stick-Y", value: offset.y });
});
j2.addEventListener("joydiv-changed", function (e) {
  var offset = joydiv2.getOneDirection().offset;
  sock.emit("input", { key: "right-stick-X", value: offset.x });
  sock.emit("input", { key: "right-stick-Y", value: offset.y });
});

// Initialize virtual controller
if (isLocal) {
  // Press the xbox button to initialize the controller!
  sock.emit("intro", { device: "x360", id: "x360", type: "x360" });

  sock.on("disconnect", () => {
    document.getElementsByTagName("img")[0].style.filter =
      "invert(29%) sepia(57%) saturate(7093%) hue-rotate(349deg) brightness(102%) contrast(70%)";
  });
  sock.on("connect", () => {
    document.getElementsByTagName("img")[0].style.filter =
      "invert(18%) sepia(88%) saturate(5119%) hue-rotate(112deg) brightness(93%) contrast(90%)";
    setTimeout(() => {
      document.getElementsByTagName("img")[0].style.filter = "invert(0)";
    }, 5000);
  });

}