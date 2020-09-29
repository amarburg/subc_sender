#!/usr/bin/env python3

import inotify.adapters
import boto3
from PIL import Image
import logging

from pathlib import Path

src_path = Path("/mnt/left_camera/Stills")


def _main():

    i = inotify.adapters.Inotify()
    i.add_watch( str(src_path) )

    for event in i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event

        logging.debug("PATH=[{}] FILENAME=[{}] EVENT_TYPES={}".format(
              path, filename, type_names))


        if 'IN_CREATE' in type_names:
            logging.info("File %s created in %s" % (filename, path) )

            try:
                image_file = Path(path) / filename
                logging.debug("Checking file %s" % image_file)
                with Image.open( str(image_file) ) as im:
                    logging.info(infile, im.format, "%dx%d" % im.size, im.mode)
            except OSError:
                pass


if __name__ == '__main__':

    logging.basicConfig( level=logging.DEBUG )

    _main()
