#!/bin/sh

sudo mount -t cifs //SubCRayfin18819/Media /mnt/left_camera -o credentials=`pwd`/credentials.txt,vers=1.0,uid=1000
sudo mount -t cifs //SubCRayfin18815/Media /mnt/right_camera -o credentials=`pwd`/credentials.txt,vers=1.0,uid=1000

mount | grep camera
