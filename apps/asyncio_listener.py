#!/usr/bin/env python3

import argparse
import ipaddress
import struct
import binascii
import socket

import asyncio

from datetime import datetime

from subc_cam import cam_config, listener

parser = argparse.ArgumentParser(description="Send SubC script to cameras")


cam_config.addDefaultArgs( parser )

args = parser.parse_args()

left_cam = cam_config.CamConfig( ipaddress.ip_address(args.left_ip), port=args.left_port, name="LEFT" )
right_cam = cam_config.CamConfig( ipaddress.ip_address(args.right_ip), port=args.right_port, name="RIGHT" )

loop = asyncio.get_event_loop()

if left_cam:
    left_task = loop.create_task( listener.camera_listener(left_cam) )

if right_cam:
    right_task = loop.create_task( listener.camera_listener(right_cam) )

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
