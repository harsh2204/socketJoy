import os
import sys
import logging
import platform
import socket
from argparse import ArgumentParser
import qrcode
import qrcode.image.svg
from xml.etree import ElementTree
import socketio
from eventlet import wsgi, listen

if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app 
    # path into variable _MEIPASS'.
    app_path= sys._MEIPASS
else:
    app_path= os.path.dirname(os.path.abspath(__file__))

# print(app_path)

if platform.system() == 'Linux':
    try:
        from nix.device import GamepadDevice
        from nix.setup import setup
    except ImportError:
        from socketjoy.nix.device import GamepadDevice
        from socketjoy.nix.setup import setup
else:
    try:
        from win.device import GamepadDevice
        from win.setup import setup
    except ImportError:
        from socketjoy.win.device import GamepadDevice
        from socketjoy.win.setup import setup

def parse_args():
    parser = ArgumentParser()
    if platform.system() == 'Linux':
        parser.add_argument(
            'user',
            nargs='?',
            default=os.getenv('SUDO_USER'),
            help='Only used with --setup. User to configure for UInput access.'
        )
    parser.add_argument(
        '-s', '--setup',
        action='store_true',
        help='Setup system for virtual device creation.'
        'Must have root/administrator access.',
    )
    parser.add_argument(
        '-H', '--host',
        default=None,
        help='Hostname or IP address the server will listen on.',
    )
    parser.add_argument(
        '-p', '--port',
        type=int, default=8022,
        help='Port the server will listen on. Defaults to 8013.',
    )
    parser.add_argument(
        '-f', '--device',
        default=None,
        help='Device to serve the application on.(eg, wlan0)'
    )
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='Print debug information.',
    )
    return parser.parse_args()


def get_logger(debug):
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO)
    logging.getLogger('engineio.server').setLevel(
        logging.INFO if debug else logging.ERROR)
    logging.getLogger('socketio.server').setLevel(
        logging.INFO if debug else logging.ERROR)
    wsgi_logger = logging.getLogger('wsgi.server')
    wsgi_logger.setLevel(
        logging.INFO if debug else logging.ERROR)
    return (logging.getLogger('socketJoy.server'), wsgi_logger)


def get_ip_address(ifname): # This function retrieves network device address from it's name (eg. wlan0)
    import fcntl
    import struct
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', bytes(ifname[:15], 'utf-8'))
    )[20:24])


def default_host(device=None):
    if device:
        try:
            return get_ip_address(device)
        except OSError as e:
            print("Something went wrong!")
            print(e)
            print("\nTrying the default hostnames")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(('1.255.255.255', 1))
        IP = sock.getsockname()[0]
    except IndexError:
        IP = '127.0.0.1'
    finally:
        sock.close()
    return IP


def main():
    args = parse_args()
    logger,  wsgi_logger = get_logger(args.debug)

    if args.setup:
        if platform.system() == 'Linux':
            setup(args.user)
        else:
            setup()
        sys.exit(0)
        return

    CLIENTS = {}
    DEVICES = {}



    static_files = {
        '/': f'{app_path}/index.html',
        '/lobby': f'{app_path}/static/lobby.html',
        '/static/js/socket.io.min.js': f'{app_path}/static/js/socket.io.min.js',
        '/static/js/socketjoy.js': f'{app_path}/static/js/socketjoy.js',
        '/static/js/joydiv.js': f'{app_path}/static/js/joydiv.js',
        '/static/css/style.css': f'{app_path}/static/css/style.css',
        '/static/css/joydiv-skin-default.css': f'{app_path}/static/css/joydiv-skin-default.css',
        '/static/socketjoy.ico':  f'{app_path}/static/favicon.ico',
        '/favicon.ico':  f'{app_path}/static/favicon.ico',
        '/static/qrcode.ico':  f'{app_path}/static/qrcode.ico',
        '/static/gh-logo.png':  f'{app_path}/static/gh-logo.png',
    }

    # create a Socket.IO server
    sio = socketio.Server(logger=args.debug, engineio_logger=args.debug, cors_allowed_origins='*',
                                ping_timeout=500) # ping_timeout(s) controls how long devices stay connected 

    app = socketio.WSGIApp(sio, static_files=static_files)


    @sio.event
    def connect(sid, environ):
        CLIENTS[sid] = environ['REMOTE_ADDR']
        logger.info(f'New client connected from {environ["REMOTE_ADDR"]}')
        logger.debug(f'Client [{CLIENTS[sid]}] : with sid: {sid}')

    @sio.event
    def intro(sid, data):
        DEVICES[sid] = GamepadDevice(data['device'], CLIENTS[sid], data['alias'])
        logger.info(
            f'Client [{CLIENTS[sid]}] : device creation complete as a {data["device"]}')
        sio.emit('controllers', [x.name for x in DEVICES.values()])

    @sio.event
    def input(sid, data):
        logger.debug(f'Received input event::{data["key"]}: {data["value"]}')
        DEVICES[sid].send(data['key'], data['value'])

    @sio.event
    def disconnect(sid):
        if sid in DEVICES:
            device = DEVICES.pop(sid)
            logger.info(f'Client [{device.address}] : disconnected (device : {device.device})')
            device.close()
        sio.emit('controllers', [x.name for x in DEVICES.values()])

    @sio.on('fetchstuff')
    def send_controllers(sid):
        sio.emit('controllers', [x.name for x in DEVICES.values()])
        sio.emit('qrcode', {'qr' : qr_img.decode('utf-8'), 'ip' : serv_ip}, room=sid)


    try:
        host = args.host or default_host(args.device)
        sock = listen((host, args.port))
    except PermissionError:
        sys.exit(
            f'Port {args.port} is not available. '
            f'Please specify a different port with -p option.'
        )

    logger.info(f'Listening on http://{host}:{args.port}/')

    serv_ip = f'http://{host}:{args.port}/' 
    qr = qrcode.QRCode(box_size=20)
    qr.add_data(serv_ip)
    if platform.system() == 'Windows':
        import colorama
        colorama.init()
    # qr.print_ascii()
    qr_img = qr.make_image(fill_color="black", back_color="white", image_factory=qrcode.image.svg.SvgImage)
    qr_img = ElementTree.tostring(qr_img._img, encoding='UTF-8', method='xml')

    wsgi.server(sock, app, log=wsgi_logger, log_output=args.debug, debug=False)



if __name__ == '__main__':
    main()
