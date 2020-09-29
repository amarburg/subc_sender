#!/bin/bash

SRC_PATH=/mnt/left_camera/
DST_PATH=/mnt/s3-nasa-invader-subc-cameras/left/

while true; do
  inotifywait -r -e modify,attrib,close_write,move,create,delete $SRC_PATH
  rsync -avW --progress --inplace --size-only  $SRC_PATH $DST_PATH
done
