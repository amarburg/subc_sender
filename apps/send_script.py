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
            self.sock.connect( (host,port) )

    def send( self, msg ):
        ## Message starts with four (little-endian) message length bytes
        outbuffer = struct.pack('<I', len(msg)) + msg.encode('ascii')

        print(binascii.hexlify(outbuffer).decode('utf-8'))

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
        return ""



left_cam = CamSender( ipaddress.ip_address('192.168.13.200'), fake=True )
right_cam = CamSender( ipaddress.ip_address('192.168.13.201'), fake=True )

parser = argparse.ArgumentParser(description="Send SubC script to cameras")

parser.add_argument("script", help="Script to send to cameras" )

args = parser.parse_args()

print("Sending script %s" % args.script )

with open(args.script) as fp:

    for n,line in enumerate(fp):
        line = line.rstrip()
        print("Line %d: %s" % (n,line))

        left_cam.connect()
        left_cam.send( line )
