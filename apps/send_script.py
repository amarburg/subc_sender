#!/usr/bin/env python3

import argparse
import ipaddress
import struct
import binascii
import socket

class CamSender:

    # 888 is the default port for the SubC Camera interface
    def __init__(self, host, port=8888, sock=None, fake=False):
        self.host = host
        self.port = port
        self.fake = fake

        if sock is None:
            self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self):
        if not self.fake:
            self.sock.connect( (str(self.host), self.port) )

    def send( self, msg ):
        ## Message starts with four (little-endian) message length bytes
        outbuffer = struct.pack('<I', len(msg)) + msg.encode('ascii')

        print(binascii.hexlify(outbuffer).decode('ascii'))

        if self.fake:
            return

        msglen = len(outbuffer)

        totalsent = 0
        while totalsent < msglen:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def receive( self ):

        if self.fake:
            return ""

        lenmsg = self.sock.recv(4)
        if lenmsg == b'':
            raise RuntimeError("socket connection broken")

        print(binascii.hexlify(lenmsg).decode('ascii'))

        a = struct.unpack('<I', lenmsg )
        msglen = a[0]

        if msglen > 256:
            raise RuntimeError("Unexpected msg length %d" % msglen)

        print("Waiting for %d bytes" % msglen)

        chunks = []
        bytes_recd = 0
        while bytes_recd < msglen:
            chunk = self.sock.recv(min(msglen - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)


parser = argparse.ArgumentParser(description="Send SubC script to cameras")

parser.add_argument("script", help="Script to send to cameras" )
parser.add_argument("--fake", action='store_true', help="Don't actually connect to cameras" )

args = parser.parse_args()

left_cam = CamSender( ipaddress.ip_address('192.168.13.234'), fake=args.fake )
right_cam = CamSender( ipaddress.ip_address('192.168.13.233'), fake=True )

print("Sending script %s" % args.script )

left_cam.connect()

while True:
    resp = left_cam.receive()
    response = resp.decode('ascii')
    print("Response: %s" % response )


#
# with open(args.script) as fp:
#
#     for n,line in enumerate(fp):
#         line = line.rstrip()
#         print("Line %d: %s" % (n,line))
#
#         left_cam.connect()
#         #left_cam.send( line )
#
