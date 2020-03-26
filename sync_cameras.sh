#!/bin/sh

DEST_DIR=/home/sysop/aaron/camera_data

mkdir $DEST_DIR/left $DEST_DIR/right

rsync -aPv /mnt/left_camera/ $DEST_DIR/left/
rsync -aPv /mnt/right_camera/ $DEST_DIR/right/
