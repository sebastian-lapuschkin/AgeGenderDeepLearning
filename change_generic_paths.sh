#!/bin/bash
#this script replaces all generic /home/ubuntu/AdienceFaces paths to he current one in all sripts.

CAFFEPATH=$(HOME)/code/caffe

#change root paths
find ./*/ -type f -exec sed -i -e s^/home/ubuntu/AdienceFaces^$HOME^g

#change caffe tools path
find ./*/ -type f -exec sed -i -e ^/home/ubuntu/repositories^$CAFFEPATH^g
