#!/usr/bin/env python3

import configargparse
import ipaddress

import asyncio

from subc_cam import cam_sender


parser = configargparse.ArgumentParser(description="Send SubC script to cameras",
                                        default_config_files=["subc_conf.yaml"])

parser.add('-c', '--my-config', is_config_file=True, help='config file path')
parser.add_argument("script", help="Script to send to cameras" )
parser.add_argument("--left-ip", default='192.168.13.228', help="IP address for left camera" )
parser.add_argument("--right-ip", default='192.168.13.234', help="IP address for right camera" )



args = parser.parse_args()

print(args)
print("----------")
print(parser.format_values())


left_cam = cam_sender.CamSender( ipaddress.ip_address(args.left_ip) )
right_cam = cam_sender.CamSender( ipaddress.ip_address(args.right_ip) )

print("Sending script %s" % args.script )

left_cam.connect()
right_cam.connect()

with open(args.script) as fp:

    for n,line in enumerate(fp):
        line = line.rstrip()
        #print("Line %d: %s" % (n,line))

        if left_cam:
            left_cam.send(line)

        if right_cam:
            right_cam.send(line)
