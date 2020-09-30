#!/bin/sh

DEST_DIR=/home/sysop/aaron/camera_data
ARGS="--recursive --progress --stats --limit-rate=500k --verbose"

s3cmd ${ARGS} sync ${DEST_DIR}/left  s3://nasa-invader-subc-cameras/left/
s3cmd ${ARGS} sync ${DEST_DIR}/right s3://nasa-invader-subc-cameras/right/
