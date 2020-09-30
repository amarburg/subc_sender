#!/bin/sh

sudo mount -t cifs //10.40.7.14/Media /mnt/left_camera -o credentials=`pwd`/credentials.txt,vers=1.0,uid=1000
sudo mount -t cifs //10.40.7.15/Media /mnt/right_camera -o credentials=`pwd`/credentials.txt,vers=1.0,uid=1000

mount | grep camera
