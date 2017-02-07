#!/bin/bash

#create necessary folders, since caffe tools do not create paths recursively
mkdir lmdb
for i in {0..4}
do
	mkdir lmdb/Test_fold_is_$i
done

#run lmdb creation scripts
find ./*/ -name "create_lmdb*.sh" -exec bash '{}' \;

#compute mean files
find ./*/ -name "make_mean*.sh" -exec bash '{}' \;
