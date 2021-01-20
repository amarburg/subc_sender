#!/usr/bin/env python3

import argparse
from subc_postprocessing import filenames
from pathlib import Path
import os

def main():

    parser = argparse.ArgumentParser(description='Rename files from SubC date format to ISO format')
    parser.add_argument('--dry-run', action="store_true",
                        help='If set, does not actually move files.')
    parser.add_argument('infile', type=Path, nargs="+",
                        help='Paths to rename')

    args = parser.parse_args()

    for infile in args.infile:

        outfile = filenames.regularize_filename( infile )

        print("Converting %s to %s" % (infile,outfile))

        if not args.dry_run:
            infile.rename(outfile)


if __name__ == "__main__":
    main()
