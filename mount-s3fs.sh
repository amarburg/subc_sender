#!/bin/sh

s3fs nasa-invader-subc-cameras /mnt/s3-nasa-invader-subc-cameras -o passwd_file=${HOME}/.passwd-s3fs -o url=https://s3.us-west-1.wasabisys.com -o uid=2000 -o gid=2000 -o umask=0007
