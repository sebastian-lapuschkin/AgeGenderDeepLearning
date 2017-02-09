#!/bin/bash

here=$PWD
flags=$here/TrainingProgressFlags-$(date +%F)
mkdir $flags

#train all models. gender models first.
cd gender_net_definitions
for i in {0..4}
do
    #create start flag. on suceess start training. on success create done flag.
    date >> $flags/gender_$i.started && caffe train --solver solver_test_fold_is_$i.prototxt && date >> $flags/gender_$i.done
done

#go back up
cd $here

#train all age models.
cd age_net_definitions
for i in {0..4}
do
    #create start flag. on suceess start training. on success create done flag.
    date >> $flags/age_$i.started && caffe train --solver solver_test_fold_is_$i.prototxt && date >> $flags/age_$i.done
done

cd $here
echo "training script terminated."
