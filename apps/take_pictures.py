#!/usr/bin/env python3

import configargparse


import subc_cam
from os import path
from datetime import datetime,timedelta
from time import sleep

import asyncio

from subc_cam import cam_config, cam_sender, listener

async def take_pictures( cams, args ):
    ltask = asyncio.create_task( listener.listen( cams ) )

    if args.pre_script:
        print("Sending pre-script %s" % args.pre_script)
        if not path.exists(args.pre_script):
            print("Pre-script %s does not exist" % args.pre_script)
            exit()

        with open(args.pre_script) as fp:
            await cam_sender.send( fp, cameras=cams )

    if args.focus:
        await cam_sender.send( ["UpdateFocus:%0.1f" % args.focus], cameras=cameras )
        sleep(1)

    repeat = args.repeat or 1
    if repeat < 0:
        repeat = 32767

    for i in range(0,repeat):
        now = datetime.now()
        picture_at = now+timedelta(seconds=args.delay)

        cmds = ["FocusDistance","TakePicture:%s" % picture_at.strftime("%H:%M:%S")]
        await cam_sender.send( cmds, cameras=cameras )

        #left_cam.send("TakePicture:%s" % (picture_at + timedelta(microseconds=0000)).strftime("%H:%M:%S.%f"))
        #right_cam.send("TakePicture:%s" % picture_at.strftime("%H:%M:%S.%f"))

        sleep(args.delay)

        if i < (repeat-1):
            print("Sleep until %s" % (datetime.now()+timedelta(seconds=args.pause)).strftime("%H:%M:%S") )
            sleep( args.pause )



    if args.post_script:
        if not path.exists(args.post_script):
            print("Post-script %s does not exist" % args.post_script)
            exit()

        with open(args.post_script) as fp:
            await cam_sender.send( fp, cameras=cameras )


    if not args.wait:
        ltask.cancel()

    try:
        await ltask
    except asyncio.CancelledError:
        return



if __name__=="__main__":
    parser = configargparse.ArgumentParser(description="Send SubC script to cameras",
                                            default_config_files=["subc_conf.yaml"])

    parser.add('-c', '--config', is_config_file=True, help='config file path')

    cam_config.addDefaultArgs( parser )

    parser.add_argument("--pre-script", default="scripts/camera_setup_iso50.subc", help="Script to run before taking pictures")
    parser.add_argument("--post-script", default=None, help="Script to run after taking pictures")

    parser.add_argument("--focus", default=None, type=float, help="Focus value to send to camera" )

    parser.add_argument("--repeat", default=None, type=int, help="Number of times to" )
    parser.add_argument("--delay", default=3, type=int, help="Number of seconds to delay before taking picture" )
    parser.add_argument("--pause", default=5, type=int, help="Pause between images" )

    parser.add_argument("--wait", action="store_true", help="Don't quit immediately, continue to listen to cameras" )


    args = parser.parse_args()

    cameras = cam_config.camsFromArgs( args )

    asyncio.run( take_pictures(cameras, args) )
