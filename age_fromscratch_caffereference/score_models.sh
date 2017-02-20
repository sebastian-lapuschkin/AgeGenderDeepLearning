#!/bin/bash
#number of iterations are adapted to test batch sizes of 50 samples, to cover the full dataset once.

for i in {0..4}
do
	echo "Age models: Scoring test fold $i on test data..."
	caffe test -model test_fold_is_$i.prototxt -weights models_test_is_$i/caffenet_train_iter_50000.caffemodel -gpu 0 -iterations 1000 > score_test_ouput_$i.txt 2>&1
	echo "Age models: Scoring test fold $i on validation data..."
	caffe test -model train_val_test_fold_is_$i.prototxt -weights models_test_is_$i/caffenet_train_iter_50000.caffemodel -gpu 0 -iterations 1000 > score_val_ouput_$i.txt 2>&1
done

