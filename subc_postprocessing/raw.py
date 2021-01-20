
import logging
import subprocess

def dng_to_png( dngpath, pngpath):
    return convert_dng(dngpath, pngpath, png_output=True)

def dng_to_jpg( dngpath, jpgpath):
    return convert_dng(dngpath, jpgpath)

def convert_dng( dngpath, pngpath, png_output=False ):

    ## Only relevant for PNGs
    # "-b8", "-n",
    if png_output:
        format_args = ["-b8", "-n"]
    else:
        format_args = ['-j']

    cmd = ["rawtherapee-cli", "-s", "-Y"] + format_args + [ "-o", str(pngpath), "-c", str(dngpath) ]
    logging.debug(cmd)

    convert_out = subprocess.run(cmd, capture_output=True)
    logging.info(convert_out.stdout.decode())
