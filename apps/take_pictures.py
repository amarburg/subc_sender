#!/usr/bin/env python3

import configargparse
import ipaddress

import asyncio

import subc_cam
from os import path
from datetime import datetime,timedelta
from time import sleep


parser = configargparse.ArgumentParser(description="Send SubC script to cameras",
                                        default_config_files=["subc_conf.yaml"])

parser.add('-c', '--config', is_config_file=True, help='config file path')
parser.add_argument("--left-ip", default='192.168.13.228', help="IP address for left camera" )
parser.add_argument("--right-ip", default='192.168.13.234', help="IP address for right camera" )

parser.add_argument("--pre-script", default="scripts/picture_setup_iso50.subc", help="Script to run before taking pictures")
parser.add_argument("--post-script", default=None, help="Script to run after taking pictures")

parser.add_argument("--repeat", default=None, type=int, help="Number of times to" )
parser.add_argument("--pause", default=5, type=int, help="Pause between images" )




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

repeat = args.repeat or 1
if repeat < 0:
    repeat = 32767

for i in range(0,repeat):
    now = datetime.now()
    picture_at = now+timedelta(seconds=2)

    #print(picture_at.strftime("%H:%M:%S"))

    cmds = ["TakePicture:%s" % picture_at.strftime("%H:%M:%S")]
    subc_cam.send( cmds, cameras=cameras )

    if i < (repeat-1):
        print("Sleep until %s" % (datetime.now()+timedelta(seconds=args.pause)).strftime("%H:%M:%S") )
        sleep( args.pause )



if args.post_script:
    if not path.exists(args.post_script):
        print("Post-script %s does not exist" % args.post_script)
        exit()

    with open(args.post_script) as fp:
        subc_cam.send( fp, cameras=cameras )
