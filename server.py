import os
import sys
import logging
import platform
import socket
from argparse import ArgumentParser
import qrcode
import socketio
# from eventlet import wsgi, listen
from aiohttp import web

if platform.system() == 'Linux':
	from nix.device import GamepadDevice
	from nix.setup import setup
else:
    try:
        from .win.device import GamepadDevice
        from .win.setup import setup
    except ImportError:from aiohttp import web

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
        type=int, default=8013,
        help='Port the server will listen on. Defaults to 8013.',
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
    aiohttp_logger = logging.getLogger('aiohttp.server')
    aiohttp_logger.setLevel(
        logging.INFO if debug else logging.ERROR)
    return (logging.getLogger('socketJoy.server'), aiohttp_logger)


def get_ip_address(ifname): # This function retrieves network device address from it's name (eg. wlan0)
    import fcntl
    import struct
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', bytes(ifname[:15], 'utf-8'))
    )[20:24])


def default_host():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(('1.255.255.255', 1))
        IP = sock.getsockname()[0]
    except IndexError:
        IP = '127.0.0.1'
    finally:
        sock.close()
    print(IP)
    return IP


def main():
    args = parse_args()
    logger,  aiohttp_logger = get_logger(args.debug)

    if args.setup:
        if platform.system() == 'Linux':
            setup(args.user)
        else:
            setup()
        sys.exit(0)
        return

    CLIENTS = {}
    DEVICES = {}

    # create a Socket.IO server
    sio = socketio.AsyncServer(logger=args.debug, engineio_logger=args.debug, cors_allowed_origins='*',
                                async_mode='aiohttp',
                                ping_timeout=500) # ping_timeout(s) controls how long devices stay connected 

    # wrap with ASGI application
    app = web.Application()
    sio.attach(app)


    @sio.event
    async def connect(sid, environ):
        CLIENTS[sid] = environ['REMOTE_ADDR']
        logger.info(f'New client connected from {environ["REMOTE_ADDR"]}')
        logger.debug(f'Client [{CLIENTS[sid]}] : with {sid=}')

    @sio.event
    async def intro(sid, data):
        DEVICES[sid] = GamepadDevice(data['device'], CLIENTS[sid])
        logger.info(
            f'Client [{CLIENTS[sid]}] : device creation complete as a {data["device"]}')

    @sio.event
    async def input(sid, data):
        logger.debug(f'Received input event::{data["key"]}: {data["value"]}')
        DEVICES[sid].send(data['key'], data['value'])

    @sio.event
    async def disconnect(sid):
        device = DEVICES.pop(sid)
        logger.info(f'Client [{device.address}] : disconnected (device : {device.device})')
        device.close()

    async def index(request):
        with open('index.html') as f:
            return web.Response(text=f.read(), content_type='text/html')
    app.router.add_static('/static', 'static')
    app.router.add_get('/', index)

    host = args.host or default_host()

    logger.info(f'Listening on http://{host}:{args.port}/')

    qr = qrcode.QRCode()
    qr.add_data(f'http://{host}:{args.port}/')
    if platform.system() == 'Windows':
        import colorama
        colorama.init()
    qr.print_ascii()

    web.run_app(app, host=args.host, port=args.port, access_log=aiohttp_logger)



if __name__ == '__main__':
    main()
