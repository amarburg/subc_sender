#!/usr/bin/env python3

import logging

import argparse
from subc_postprocessing import raw
from pathlib import Path
import os

def main():

    logging.basicConfig( level=logging.DEBUG )

    parser = argparse.ArgumentParser(description='Process many dng files into pngs')
    parser.add_argument('--dry-run', action="store_true",
                        help='If set, does not actually move files.')
    parser.add_argument("--png", action="store_true",help="If set, create PNG rather than JPG")
    parser.add_argument("--dest-dir", default=Path.cwd(), type=Path, help='Directory for converted files')
    parser.add_argument('infile', type=Path, nargs="+",
                        help='Paths to rename')

    args = parser.parse_args()

    if not args.dest_dir.is_dir():
        print("Destination %s does not exist or is not a directory" % (args.dest_dir))

    if args.png:
        extension = ".png"
    else:
        extension = ".jpg"

    for infile in args.infile:

        outfile = args.dest_dir / infile.with_suffix(extension).name
        print("Converting %s to %s" % (infile,outfile))

        if not args.dry_run:

            raw.dng_to_png( infile, outfile )


if __name__ == "__main__":
    main()
