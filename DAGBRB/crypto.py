# -*- coding: utf8 -*-
import binascii
# import sha3
import socket
#rom Crypto.Hash import keccak
import sys

# def keccak256(s):
#     # k = sha3.keccak_256()
#     k = keccak.new(digest_bits=256)
#     k.update(s)
#     return k.digest()


def int_to_big_endian(large_num):
    """
    :param large_num: int | long
    :return: byte string (str)
    """
    if large_num == 0:
        return b'\x00'

    s = hex(large_num)  # got hex string of number: '0x499602d2'
    s = s[2:]  # remove prefix '0x': '499602d2'
    s = s.rstrip('L')  # remove postfix of long number 'L': '499602d2'
    if len(s) & 1:  # if the string length is odd, align to even by add prefix '0': '499602d2'
        s = '0' + s

    s = binascii.a2b_hex(s)  # convert ascii string to byte string

    return s


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip

class Logger(object):
    def __init__(self, filename='default.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'w')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass