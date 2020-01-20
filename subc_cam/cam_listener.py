#!/usr/bin/env python3

import argparse
import ipaddress
import struct
import binascii
import socket

import asyncio

from datetime import datetime

async def camera_listener( cam ):
    reader,writer = await asyncio.open_connection( str(cam.host), cam.port )

    while True:
        #print("% 5s: Waiting..." % cam.name )

        lenmsg = await reader.read(4)
        if lenmsg == b'':
            raise RuntimeError("socket connection broken")

        #print(binascii.hexlify(lenmsg).decode('ascii'))

        a = struct.unpack('<I', lenmsg )
        msglen = a[0]

        #print("% 5s: Waiting for %d bytes" % (cam.name, msglen))

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

        now = datetime.now().strftime("%H:%M:%S.%f")
        print("% 9s | % 5s (%3d) ---> %s" % (now, cam.name, msglen, response) )

async def listen( cameras ):

    tasks = [asyncio.create_task( camera_listener(cam) ) for cam in cameras]

    ## Now what?
    while True:
        await asyncio.gather(*tasks)
