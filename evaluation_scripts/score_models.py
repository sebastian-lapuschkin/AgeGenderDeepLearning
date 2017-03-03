print 'import: matplotlib.pyplot';  import matplotlib.pyplot as plt
print 'import: numpy';              import numpy as np
print 'import: caffe';              import caffe
print 'import: caffe.proto';        from caffe.proto import caffe_pb2
print 'import: lmdb';               import lmdb
print 'import: time';               import time

def score_model(lmdb_path,meanimg_path,prototxt_path,modelweight_path,inputsize):

    #create classifier
    print 'loading/parsing mean file'
    mean = caffe.io.caffe_pb2.BlobProto.FromString(open(meanimg_path,'rb').read())
    mean = caffe.io.blobproto_to_array(mean)[0]
    #mean = np.transpose(mean,[0,2,1])
    print mean.shape

    print 'creating model'
    caffe.set_mode_gpu() #considerably faster

    net = caffe.Net(prototxt_path, modelweight_path, caffe.TEST )
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_mean('data', mean.mean(1).mean(1))
    transformer.set_transpose('data',[2,0,1])
    transformer.set_channel_swap('data',[2,1,0])
    #transformer.set_raw_scale('data',255.) #this broke the prediction.
    #net.blobs['data'].reshape(1,3,inputsize,inputsize) # prediction in batch sizes of 1 #redundant here



    #open lmdb file
    print 'opening lmdb file'
    lmdb_env = lmdb.open(lmdb_path)
    lmdb_txn = lmdb_env.begin()
    lmdb_cursor = lmdb_txn.cursor()
    datum = caffe_pb2.Datum()
    lmdb_size = lmdb_txn.stat()['entries']

    hit=0.0;                hit1off = 0.0
    oversample_hit=0.0 ;    oversample_hit1off = 0.0
    singletime=0.0 ; oversample_time = 0.0
    count=0.0
    #read lmdb filen entries
    print 'reading lmdb file entries'
    for key, value in lmdb_cursor:
        datum.ParseFromString(value)

        label = datum.label
        im = caffe.io.datum_to_array(datum).astype(np.uint8)
        im = np.transpose(im,(1,2,0)) # from (dim, row, col) to (row,col,dim) #for visualization
        im = im[...,::-1] # from BGR to RGB #for visualization

        single_start = time.time()
        net.blobs['data'].reshape(1,3,inputsize,inputsize) #reset buffer size, since we also do oversampling evaluation
        net.blobs['data'].data[...] = transformer.preprocess('data',im)

        #standard one-sample-prediction
        output = net.forward()

        if inputsize == 227: # Adience or BVLC reference net
            prediction = output['prob'].argmax()
        elif inputsize == 224: # googlenet
            prediction = output['loss3/loss3'].argmax()

        hit += (label == prediction)
        hit1off += (np.abs(label - prediction) <= 1)
        singletime += time.time() - single_start


        #oversampling prediction
        oversampling_start = time.time()

        net.blobs['data'].reshape(10,3,inputsize,inputsize)
        ims = caffe.io.oversample([im],(inputsize,inputsize))
        for i in xrange(len(ims)): #probably batch-executable somehow.
            net.blobs['data'].data[i,...] = transformer.preprocess('data',ims[i])

        oversample_outputs = net.forward()
        if inputsize == 227:
            oversample_prediction = output['prob'].mean(axis=0).argmax()
        elif inputsize == 224:
            oversample_prediction = output['loss3/loss3'].mean(axis=0).argmax()

        oversample_hit += (label == oversample_prediction)
        oversample_hit1off += (np.abs(label - oversample_prediction) <= 1)
        oversample_time += time.time() - oversampling_start

        count += 1 #count number of evaluated samples


        #print status every 100 and with the last sample
        if count % 20 == 0 or count == lmdb_size:
            print 'Evaluated model performance after {}/{} samples:'.format(int(count),lmdb_size)
            print 'SINGLE -- ACC: {}, 1-OFF: {} ({} images/s)'.format(np.round(100 * hit / count,2),np.round(100* hit1off / count,2), np.round(count/singletime,2))
            print 'OVRSMP -- ACC: {}, 1-OFF: {} ({} images/s)'.format(np.round(100 * oversample_hit / count,2),np.round(100* oversample_hit1off / count,2),np.round(count/oversample_time,2))

        '''
        #for visualization
        plt.imshow(im)
        plt.title('L:{} P:{}'.format(label,prediction))
        plt.show()
        '''

    return {'acc': hit/count, '1off': hit1off/count, 'acco':oversample_hit/count, '1offo':oversample_hit1off/count}










''' MAIN '''


testfold = 0
modeliteration = 50000
ageorgender = 'age'
traintestval = 'test'
#modelpostfix = 'net_definitions'
modelpostfix = 'finetuning_caffereference'
inputsize=227

#modelpostfix = 'finetuning_googlenet'
#inputsize=224

PATHPREFIX = '/home/lapuschkin/Desktop/FaceRecognition/code/AgeGenderDeepLearning'
lmdb_path = PATHPREFIX + '/lmdb/Test_fold_is_{}/{}_{}_lmdb'.format(testfold,ageorgender,traintestval)
meanimg_path = PATHPREFIX + '/mean_image/Test_fold_is_{}/mean.binaryproto'.format(testfold)
prototxt_path = PATHPREFIX + '/{}_{}/deploy.prototxt'.format(ageorgender,modelpostfix)
modelweight_path = PATHPREFIX + '/{}_{}/models_test_is_{}/caffenet_train_iter_{}.caffemodel'.format(ageorgender,modelpostfix,testfold,modeliteration)


score_model(lmdb_path,meanimg_path,prototxt_path,modelweight_path,inputsize)
