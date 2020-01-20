#!/usr/bin/env python3

import configargparse
import argparse

import subc_cam
from os import path
from datetime import datetime,timedelta
from time import sleep

import numpy as np

import asyncio
from subc_cam import cam_config, cam_sender, cam_listener

async def focus_sweep( cams, args ):
    listener = asyncio.create_task( cam_listener.listen( cams ) )
    sender = cam_sender.CamSender( cams )

    if args.pre_script:
        if not path.exists(args.pre_script):
            print("Pre-script %s does not exist" % args.pre_script)
            exit()

        with open(args.pre_script) as fp:
            await sender.send( fp )


    foci = np.arange( args.focus_start, args.focus_stop, args.focus_step )

    for focus in foci:

        #print(picture_at.strftime("%H:%M:%S"))

        cmds = ["FocusDistance",
                "UpdateFocus:%.1f" % focus]
        await sender.send( cmds )

        await asyncio.sleep(1)

        now = datetime.now()
        picture_at = now+timedelta(seconds=args.delay)

        # cmds = [ ]
        # subc_cam.send( cmds, cameras=cameras )

        await sender.send( ["TakePicture:%s" % picture_at.strftime("%H:%M:%S.%f")] )

        await asyncio.sleep( args.delay )

        cmds = ["FocusDistance"]
        await sender.send( cmds )

        if focus != foci[-1]:

            print("Sleep until %s" % (picture_at+timedelta(seconds=args.pause)).strftime("%H:%M:%S") )
            await asyncio.sleep( args.pause )



    if args.post_script:
        if not path.exists(args.post_script):
            print("Post-script %s does not exist" % args.post_script)
            exit()

        with open(args.post_script) as fp:
            await sender.send( fp )


    if not args.wait:
        listener.cancel()

    try:
        await listener
    except asyncio.CancelledError:
        return

if __name__=="__main__":

    parser = configargparse.ArgumentParser(description="Send SubC script to cameras",
                                            default_config_files=["subc_conf.yaml"])
    parser.add('-c', "--config", is_config_file=True, help='config file path')

    cam_config.addDefaultArgs( parser )

    parser.add_argument("--pre-script", default="scripts/camera_setup_iso50.subc", help="Script to run before taking pictures")
    parser.add_argument("--post-script", default=None, help="Script to run after taking pictures")

    parser.add_argument("--delay", default=3, type=int, help="Number of seconds to delay before taking picture" )
    parser.add_argument("--pause", default=5, type=int, help="Pause between images" )

    parser.add_argument("--wait", action="store_true", help="Don't quit immediately, continue to listen to cameras" )

    parser.add_argument("--focus-start", required=True, type=float, help="Minimum focus distance")
    parser.add_argument("--focus-stop", required=True, type=float, help="Maximum focus distance")
    parser.add_argument("--focus-step", required=True, type=float, help="Step in focus distance")

    args = parser.parse_args()

    cameras = cam_config.camsFromArgs( args )

    asyncio.run( focus_sweep(cameras, args) )
