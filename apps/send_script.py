#!/usr/bin/env python3

import argparse
import ipaddress
import struct
import binascii
import socket

import asyncio

from subc_cam import cam_config, cam_sender, listener

async def send( fp, cams, wait = False ):
    ltask = asyncio.create_task( listener.listen( cams ) )

    await cam_sender.send( fp, cams )

    if not args.wait:
        ltask.cancel()

    try:
        await ltask
    except asyncio.CancelledError:
        return


if __name__=="__main__":

    parser = argparse.ArgumentParser(description="Send SubC script to cameras")
    cam_config.addDefaultArgs( parser )

    parser.add_argument("script", help="Script to send to cameras" )
    parser.add_argument("--wait", action="store_true", help="Don't quit immediately, continue to listen to cameras" )
    args = parser.parse_args()

    cameras = cam_config.camsFromArgs( args )

    print("Sending script %s" % args.script )

    with open(args.script) as fp:
        asyncio.run(send( fp, cams=cameras, wait=args.wait ))
