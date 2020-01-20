#!/usr/bin/env python3

import configargparse
import ipaddress

import asyncio

import subc_cam
from os import path
from datetime import datetime,timedelta
from time import sleep

import numpy as np


parser = configargparse.ArgumentParser(description="Send SubC script to cameras",
                                        default_config_files=["subc_conf.yaml"])

parser.add('-c', '--config', is_config_file=True, help='config file path')
parser.add_argument("--left-ip", default='192.168.13.228', help="IP address for left camera" )
parser.add_argument("--right-ip", default='192.168.13.234', help="IP address for right camera" )

parser.add_argument("--pre-script", default="scripts/picture_setup_iso50.subc", help="Script to run before taking pictures")
parser.add_argument("--post-script", default=None, help="Script to run after taking pictures")

parser.add_argument("--pause", default=2, type=int, help="Pause between images" )
parser.add_argument("--delay", default=3, type=int, help="Number of seconds to delay before taking picture" )

parser.add_argument("--focus-start", type=float, help="Minimum focus distance")
parser.add_argument("--focus-stop", type=float, help="Maximum focus distance")
parser.add_argument("--focus-step", type=float, help="Step in focus distance")

args = parser.parse_args()

# print(args)
# print("----------")
# print(parser.format_values())

left_cam = subc_cam.CamSender( ipaddress.ip_address(args.left_ip) )
right_cam = subc_cam.CamSender( ipaddress.ip_address(args.right_ip) )

cameras = [left_cam,right_cam]

left_cam.connect()
right_cam.connect()

if args.pre_script:
    if not path.exists(args.pre_script):
        print("Pre-script %s does not exist" % args.pre_script)
        exit()

    with open(args.pre_script) as fp:
        subc_cam.send( fp, cameras=cameras )


foci = np.arange( args.focus_start, args.focus_stop, args.focus_step )

for focus in foci:

    #print(picture_at.strftime("%H:%M:%S"))

    cmds = ["FocusDistance",
            "UpdateFocus:%.1f" % focus]
    subc_cam.send( cmds, cameras=cameras )

    sleep(1)

    now = datetime.now()
    picture_at = now+timedelta(seconds=args.delay)

    # cmds = [ ]
    # subc_cam.send( cmds, cameras=cameras )

    left_cam.send("TakePicture:%s" % picture_at.strftime("%H:%M:%S.%f"))
    right_cam.send("TakePicture:%s" % picture_at.strftime("%H:%M:%S.%f"))

    sleep( args.delay )

    cmds = ["FocusDistance"]
    subc_cam.send( cmds, cameras=cameras )

    if focus != foci[-1]:

        print("Sleep until %s" % (picture_at+timedelta(seconds=args.pause)).strftime("%H:%M:%S") )
        sleep( args.pause )



if args.post_script:
    if not path.exists(args.post_script):
        print("Post-script %s does not exist" % args.post_script)
        exit()

    with open(args.post_script) as fp:
        subc_cam.send( fp, cameras=cameras )
