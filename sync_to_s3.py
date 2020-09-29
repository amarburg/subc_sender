#!/usr/bin/env python3

import time
import boto3
from botocore.exceptions import ClientError
from PIL import Image
import logging
from tempfile import TemporaryDirectory
import subprocess
import re

from pathlib import Path
from datetime import datetime, timedelta

from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler

left_paths = [ Path("/mnt/left_camera/Stills") ]

right_path = Path("/mnt/right_camera/Stills")

def dng_to_png( dngpath, pngpath ):

    cmd = ["convert", dngpath, pngpath]
    logging.debug(cmd)

    convert_out = subprocess.run(cmd, capture_output=True)
    logging.info(convert_out.stdout.decode())

def subc_file_to_datetime( filename ):
    ## Isolate just the file name itself
    filename = filename.name

    return datetime.strptime(filename, "%Y.%m.%d %H.%M.%S.%f.dng")

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

        left_date = subc_file_to_datetime( newfile )
        logging.debug("   detected new left raw file %s with date %s" % (newfile, left_date) )

        # Look for matching right image
        ## restrict to images from today
        right_glob = "%04d.%d.%d*.dng" % (left_date.year, left_date.month, left_date.day)
        right_files = right_path.glob(right_glob)

        pair = ImagePair(newfile)

        for right_file in right_files:
            logging.debug(right_file)

            right_date = subc_file_to_datetime( right_file )

            if abs(right_date - left_date) < timedelta(seconds=1):
                logging.info("Found matching rightfile %s" %right_file)

                pair.right = right_file
                break

        else:
            logging.error( "Did not find matching right file")



        def convert_and_upload( file, label ):

            #with TemporaryDirectory() as td:

            dngfile = Path("/tmp") / Path(file.name)
            shutil.copy( file, dngfile )

            pngfile = dngfile.with_suffix(".png")

            dng_to_png( dngfile, pngfile )

            # Upload the file
            s3_client = boto3.client('s3')
            bucket = "nasa-invader-subc-cameras"
            object_name = Path(label) / pngfile.name

            try:
                response = s3_client.upload_file( str(pngfile), bucket, str(object_name) )
            except ClientError as e:
                logging.error(e)
                return False
            return True


        convert_and_upload( pair.left, "left" )
        if pair.right:
            convert_and_upload( pair.right, "right" )


if __name__ == '__main__':

    logging.basicConfig( level=logging.DEBUG )

    event_handler = SubcEventHandler()

    observer = PollingObserver()
    for p in left_paths:
        logging.debug("Watching %s" % p)
        observer.schedule(event_handler, str(p) )

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
