# AgeGenderDeepLearning

##Description
The purpose of this repository is to assist readers in reproducing our results on age and gender classification for facial images as described in the following work:

Gil Levi and Tal Hassner, Age and Gender Classification Using Convolutional Neural Networks, IEEE Workshop on Analysis and Modeling of Faces and Gestures (AMFG), at the IEEE Conf. on Computer Vision and Pattern Recognition (CVPR), Boston, June 2015

Project page: http://www.openu.ac.il/home/hassner/projects/cnn_agegender/

The code contains the original meta-data files with age and gender labels, a python script for creating prototxt file in order to create the lmdb's for training and shell files for creating the lmdb and mean images. 


If you find our models or code useful, please add suitable reference to our paper in your work.


---
Copyright 2015, Gil Levi and Tal Hassner 

The SOFTWARE provided in this page is provided "as is", without any guarantee made as to its suitability or fitness for any particular use. It may contain bugs, so use of this tool is at your own risk. We take no responsibility for any damage of any sort that may unintentionally be caused through its use. 

##Changes made in this fork
Added some scripts to automatically fix paths, to execute data generation and to run model training. Assuming you have your data downloaded and available (since there are some manual steps involved anyway), execute the following steps

        0) Adjust CAFFEPATH in change_generic_paths.sh
        1) run bash change_generic_paths.sh
        2) Place and extract the data archives downloaded from the Adience data download page in DATA/
        3) run bash run_all_datagen_scripts.sh
        4) run train_all_models.sh
