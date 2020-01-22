#!/usr/bin/env python3

import argparse
import ipaddress
import struct
import binascii
import socket

import asyncio

from datetime import datetime

from subc_cam import cam_config, cam_listener

if __name__=="__main__":

    parser = argparse.ArgumentParser(description="Send SubC script to cameras")

    cam_config.addDefaultArgs( parser )

    args = parser.parse_args()

    left_cam = cam_config.CamConfig( ipaddress.ip_address(args.left_ip), port=args.left_port, name="LEFT" )
    right_cam = cam_config.CamConfig( ipaddress.ip_address(args.right_ip), port=args.right_port, name="RIGHT" )

    asyncio.run( cam_listener.listen( [left_cam, right_cam] ) )
