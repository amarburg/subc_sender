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
    parser.add_argument("--wait", action="store_true" )
    args = parser.parse_args()

    left_cam = cam_config.CamConfig( ipaddress.ip_address(args.left_ip), port=args.left_port, name="LEFT" )
    right_cam = cam_config.CamConfig( ipaddress.ip_address(args.right_ip), port=args.right_port, name="RIGHT" )

    print("Sending script %s" % args.script )

    with open(args.script) as fp:
        asyncio.run(send( fp, cams=[left_cam,right_cam], wait=args.wait ))
