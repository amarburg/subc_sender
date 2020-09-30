#!/usr/bin/env python3

import argparse
import ipaddress
import struct
import binascii
import random

import asyncio


canned_responses = [ b'NTPClockDrift:-5.16E-05',
                     b'CPUTemp:425' ]


parser = argparse.ArgumentParser(description="SubC camera simulator")
parser.add_argument("--port", default=8889, help="Don't actually connect to cameras" )
args = parser.parse_args()

async def camera_simulator(reader, writer):

    done = False

    print("Accepting connection...")

    while not done:

        msg = random.choice( canned_responses )
        outbuffer = struct.pack('<I', len(msg)) + msg

        writer.write(outbuffer)

        try:
            await writer.drain()
            data = await reader.read(255)

            ## Drop length (for now)
            data = data[4:].decode('ascii')

            print("Received (%d): %s" % (len(data),data))
        except ConnectionResetError:
            break;

        if writer.is_closing():
            break;

        await asyncio.sleep(1)

    print("Closing the connection")
    writer.close()

async def main( port=8888 ):
    server = await asyncio.start_server(
        camera_simulator, '127.0.0.1', port)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

if __name__=="__main__":
    asyncio.run(main(args.port))
