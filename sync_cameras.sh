#!/bin/sh

DEST_DIR=/zvol1/aaron/subc_sync

mkdir $DEST_DIR/left $DEST_DIR/right

rsync -aPv /mnt/left_camera/ $DEST_DIR/left/
rsync -aPv /mnt/right_camera/ $DEST_DIR/right/
