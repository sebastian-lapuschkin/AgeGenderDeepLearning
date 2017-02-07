#!/bin/bash
#this script replaces all generic /home/ubuntu/AdienceFaces paths to he current one in all sripts.

CAFFEPATH=$HOME/code/caffe

#change root paths
find ./*/ -type f -exec sed -i -e s^/home/ubuntu/AdienceFaces^$PWD^g '{}' \;

#change caffe tools path 
find ./*/ -type f -exec sed -i -e s^/home/ubuntu/repositories/caffe^$CAFFEPATH^g '{}' \;
