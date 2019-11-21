#!/usr/bin/env python3

import argparse
import ipaddress
import struct
import binascii
import socket

import asyncio

class CamSender:

    # 888 is the default port for the SubC Camera interface
    def __init__(self, host, name="", port=8888, fake=False):
        self.host = host
        self.port = port
        self.fake = fake
        self.name = name

        # if sock is None:
        #     self.sock = socket.socket(
        #                     socket.AF_INET, socket.SOCK_STREAM)
        # else:
        #     self.sock = sock

#
#     async def connect(self):
#         if not self.fake:
#             self.reader,self.writer = await asyncio.open_connection( str(self.host), self.port )
#
#     async def send( self, msg ):
#         ## Message starts with four (little-endian) message length bytes
#         outbuffer = struct.pack('<I', len(msg)) + msg.encode('ascii')
#
#         print(binascii.hexlify(outbuffer).decode('ascii'))
#
#         if self.fake:
#             return
#
#         msglen = len(outbuffer)
#
#         totalsent = 0
#         while totalsent < msglen:
#             sent = self.writer.write(msg[totalsent:])
#             if sent == 0:
#                 raise RuntimeError("socket connection broken")
#             totalsent = totalsent + sent
#
#     async def receive( self ):
#
#         if self.fake:
#             return ""
#
#         lenmsg = await self.reader.read(4)
#         if lenmsg == b'':
#             raise RuntimeError("socket connection broken")
#
#         #print(binascii.hexlify(lenmsg).decode('ascii'))
#
#         a = struct.unpack('<I', lenmsg )
#         msglen = a[0]
#
#         if msglen > 256:
#             raise RuntimeError("Unexpected msg length %d" % msglen)
#
#         #print("Waiting for %d bytes" % msglen)
#
#         chunks = []
#         bytes_recd = 0
#         while bytes_recd < msglen:
#             chunk = await self.reader.read(min(msglen - bytes_recd, 2048))
#             if chunk == b'':
#                 raise RuntimeError("socket connection broken")
#             chunks.append(chunk)
#             bytes_recd = bytes_recd + len(chunk)
#         return b''.join(chunks)


async def camera_listener( cam ):
    reader,writer = await asyncio.open_connection( str(cam.host), cam.port )

    print("Listening to %s" % cam.name )

    while True:

        lenmsg = await reader.read(4)
        if lenmsg == b'':
            raise RuntimeError("socket connection broken")

        #print(binascii.hexlify(lenmsg).decode('ascii'))

        a = struct.unpack('<I', lenmsg )
        msglen = a[0]

        if msglen > 256:
            raise RuntimeError("Unexpected msg length %d" % msglen)

        #print("Waiting for %d bytes" % msglen)

        chunks = []
        bytes_recd = 0
        while bytes_recd < msglen:
            chunk = await reader.read(min(msglen - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)

        resp = b''.join(chunks)
        response = resp.decode('ascii')
        print("% 5s (%3d): %s" % (cam.name, msglen, response) )


parser = argparse.ArgumentParser(description="Send SubC script to cameras")

#parser.add_argument("script", help="Script to send to cameras" )
parser.add_argument("--fake", action='store_true', help="Don't actually connect to cameras" )

args = parser.parse_args()

left_cam = CamSender( ipaddress.ip_address('192.168.13.234'), name="LEFT", fake=args.fake )
right_cam = CamSender( ipaddress.ip_address('127.0.0.1'), port=8889, name="RIGHT" )

loop = asyncio.get_event_loop()

if left_cam:
    left_task = loop.create_task( camera_listener(left_cam) )

if right_cam:
    right_task = loop.create_task( camera_listener(right_cam) )

loop.run_forever()



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
