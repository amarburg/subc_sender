#!/usr/bin/env python3

# Uploads files to http://invader-cameras.camhd.science/

import os
import time
import boto3
from botocore.exceptions import ClientError
from PIL import Image
import logging
from tempfile import TemporaryDirectory
import re
import shutil
import subprocess

from pathlib import Path
from datetime import datetime, timedelta

from subc_postprocessing import filenames, raw

from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler

left_paths = [ Path("/mnt/left_camera/Stills") ]
right_paths = [ Path("/mnt/right_camera/Stills"), Path("/mnt/right_camera/Stills_1") ]


def wait_until_readable( fname, timeout=10 ):
    if timeout < 0:
        return false

    for x in range(0,timeout):
        if os.access(fname, os.R_OK):
            break

        logging.debug("Can't read, waiting...")
        time.sleep(1)

    return os.access(fname, os.R_OK)


def convert_and_upload( file, label ):

    with TemporaryDirectory() as td:

        dngfile = "/tmp/" / Path(file.name)
        logging.debug("Copying %s to %s" % (file,dngfile))

        cmd = ["cp", file, dngfile ]
        subprocess.run(cmd)

        regfile = filenames.regularize_filename(dngfile)
        logging.debug(regfile)
        jpgfile = regfile.with_suffix(".jpg")
        logging.debug("Converting %s to %s" % (dngfile,jpgfile))

        raw.dng_to_jpg( dngfile, jpgfile )

        # Upload the file
        s3_client = boto3.client('s3',endpoint_url = 'https://s3.us-west-1.wasabisys.com')
        bucket = "nasa-invader-subc-cameras"
        object_name = Path(label) / jpgfile.name

        try:
            response = s3_client.upload_file( str(jpgfile), bucket, str(object_name) )
        except ClientError as e:
            logging.error(e)
            return False
        return True


class ImagePair:

    def __init__(self,left):
        self.left = left
        self.right = None

class SubcEventHandler( FileSystemEventHandler ):

    def on_created(self, event):
        super(SubcEventHandler, self).on_created(event)

        what = 'directory' if event.is_directory else 'file'
        logging.info("Created %s: %s", what, event.src_path)

        newfile = Path(event.src_path)
        if newfile.suffix != ".dng":
            return

        try:
            left_date = filenames.subc_file_to_datetime( newfile )
        except ValueError as err:
            logging.warning("Unable to parse subc file name: %s" % err)
            return

        logging.debug("   detected new left raw file %s with date %s" % (newfile, left_date) )

        # Look for matching right image
        ## restrict to images from today
        right_glob = "%04d.%d.%d*.dng" % (left_date.year, left_date.month, left_date.day)

        right_files = [p.glob(right_glob) for p in right_paths]
        right_files = [f for p in right_files for f in p]

        pair = ImagePair(newfile)

        for right_file in right_files:

            right_date = filenames.subc_file_to_datetime( right_file )

            if abs(right_date - left_date) < timedelta(seconds=1):
                logging.info("Found matching rightfile %s" % right_file)

                pair.right = right_file
                break

        else:
            logging.error( "Did not find matching right file")


        if not wait_until_readable( pair.left ):
            logging.error("Never became readable, skipping...")
            return

        convert_and_upload( pair.left, "left" )
        if pair.right:

            if not wait_until_readable( pair.right ):
                logging.error("Never became readable, skipping...")
                return

            convert_and_upload( pair.right, "right" )

            ## Build composite


if __name__ == '__main__':

    logger = logging.getLogger(__name__)
    logging.basicConfig( level=logging.DEBUG )

    ## Squelch boto-related logging output
    for name in logging.Logger.manager.loggerDict.keys():
        if ('boto' in name) or ('urllib3' in name) or ('s3transfer' in name) or ('boto3' in name) or ('botocore' in name) or ('nose' in name):
            logging.info("Setting logger for %s to CRITICAL" % name)
            logging.getLogger(name).setLevel(logging.CRITICAL)


    event_handler = SubcEventHandler()

    observer = PollingObserver()
    for p in left_paths:
        logging.debug("Watching %s" % p)
        observer.schedule(event_handler, str(p) )

    # for p in right_paths:
    #     logging.debug("Watching %s" % p)
    #     observer.schedule(event_handler, str(p) )

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
