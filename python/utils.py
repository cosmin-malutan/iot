
import socket
import fcntl
import struct
import time

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.

def get_ip_address(ifname):
    ip = False
    while (ip == False):
        try:
            ip = _get_ip_address(ifname)
        except Exception as e:
            print(e)
            time.sleep(1)
    return ip

def _get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])