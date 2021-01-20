#!/bin/sh

ARGS="--recursive --progress --stats --limit-rate=500k --verbose"

s3cmd ${ARGS} sync /mnt/left_camera/Stills*  s3://nasa-invader-subc-cameras/raw/left/
s3cmd ${ARGS} sync /mnt/right_camnera/Stills* s3://nasa-invader-subc-cameras/raw/right/
