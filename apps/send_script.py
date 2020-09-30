#!/usr/bin/env python3

import argparse
import ipaddress
import struct
import binascii
import socket
import fileinput
import asyncio

import sys

from subc_cam import cam_config, cam_sender, cam_listener

async def send( fp, cams, wait = False ):
    listener = asyncio.create_task( cam_listener.listen( cams ) )

    sender = cam_sender.CamSender( cams )

    await sender.send( fp )

    if not wait:
        listener.cancel()

    try:
        await listener
    except asyncio.CancelledError:
        return


if __name__=="__main__":

    parser = argparse.ArgumentParser(description="Send SubC script to cameras")
    cam_config.addDefaultArgs( parser )

    parser.add_argument("script", nargs="*", help="Script to send to cameras, use \"--\" for stdin" )
    parser.add_argument('-i','--stdin', help="Send from stdin", action="store_true", dest="stdin")
    parser.add_argument("--wait", action="store_true", help="Don't quit immediately, continue to listen to cameras" )
    args = parser.parse_args()

    cameras = cam_config.camsFromArgs( args )

    if args.stdin:
        print("Sending from stdin")
        asyncio.run(send( sys.stdin, cams=cameras, wait=args.wait ))
    else:
        for n,script in enumerate(args.script):
            print("Sending script %s" % script )
            with open(script) as fp:

                ## Only wait on last script ...
                ## \todo Probably a much more Pythonic way to do this....
                wait = args.wait
                if n < len(args.script)-1:
                    wait = False

                asyncio.run(send( fp, cams=cameras, wait=wait ))
