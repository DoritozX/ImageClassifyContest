##-*- coding:utf8*-
import tensorflow as tf
import os
import re
from PIL import Image
from module import *

def readAllFilesWithTag():
    #read the train tag file(.tsv)
    classesFile = selectFile()
    classesDF = readCsvFile(classesFile[0])
    classes = getClassesTag(classesDF)
    #choose the training sample folder
    trainDir = selectFolder()
    #choose the training sample files
    trainFileList = os.listdir(trainDir)
    #use the lambda to re-sort the files
    pattern = re.compile('(\\w+)_(\\d+).(\\w+)')
    trainFileList.sort(key = lambda x:int(pattern.match(x).groups()[1]))

    return trainFileList, classes

def generateDataSet(trainFileList, classes):
    import random

    if not len(trainFileList) == len(classes):
        raise ValueError("Different length of data set and the tag.") 
        return
    else:
        dataLength = len(trainFileList)
        randomSample = 2000
        randomIndex = random.sample(range(0, dataLength), randomSample)

        trainFileListRand = trainFileList[randomIndex]
        classesRand = classes[randomIndex]

        return trainFileListRand, classesRand

def convert2bin(binFileName):
    """
    convert the training files int binary format
    binFileName: "xxxx.tfrecords"
    """
    
    #convert to the binary file
    writer = tf.python_io.TFRecordWriter(binFileName)

    for index, fileName in enumerate(trainFileList):
        absPath = trainDir + '\\' + fileName
        img = Image.open(absPath)
        img = img.resize((667, 667))
        img_binary = img.tobytes()
        example = tf.train.Example(features = tf.train.Features(feature = {"label": tf.train.Feature(int64_list = tf.train.Int64List(value = [int(classes[index])])),\
                                                                           "img_raw": tf.train.Feature(bytes_list = tf.train.BytesList(value = [img_binary]))}))
        writer.write(example.SerializeToString())
        print(fileName, " has been read...")

    writer.close()
    return

def readDecode(binFileName, numEpochs = 1):
    """
    read the training files which is binary format
    and convert it into "labels" and "image"
    """
    fileName = tf.train.string_input_producer([binFileName], num_epochs = numEpochs)
    reader = tf.TFRecordReader()
    _, serializedExample = reader.read(fileName)
    features = tf.parse_single_example(serializedExample,\
                                       features = {"label": tf.FixedLenFeature([], tf.int64),\
                                                   "img_raw": tf.FixedLenFeature([], tf.string),\
                                                   })
    image = tf.decode_raw(features["img_raw"], tf.uint8)
    image = tf.reshape(image, [667,667,3])
    image = tf.cast(image, tf.float32) * (1./255) - 0.5
    label = tf.cast(features['label'], tf.int32)

    return image, label
    
def inputs(batchSize, numEpochs):
    #input parameter:
    #   train: choose the input training/valid data
    #   batchSize: data number in each batch
    #   numEpochs: training times. if 0 or None means no stop
    """
    make the training sample randomly and get a minimized batch tensor by using the tf.train.shuffle_batch

    return value: A tuple(images, labels)
     * images: type float, shape[batchSize, [224,224,3], range[-0.5, 0.5]]
     * labels: type int32, shape[batchSize], range[0, len(classes)]
     notice: tf.train.QueueRunner must use the tf.train.start_queue_runners() to start the thread
    """
    if not numEpochs:
        numEpochs = None
    #choose the binary file
    fileName = selectFile()
    image, label = readDecode(fileName[0], numEpochs)
    #make the example randomly and regular them to the batch_size
    #generate the RandomShuffleQueue by the tf.train.shuffle_batch, and open 2 threads
    image, sparseLabels = tf.train.shuffle_batch([image, label],\
                                                 batch_size = batchSize,\
                                                 num_threads = 2,\
                                                 capacity = 1000 + 3 * batchSize,\
                                                 #keep a part of queue to ensure that has enough data to shuffle 
                                                 min_after_dequeue = 1000,\
                                                 )

    return image, sparseLabels

#def runTraining():
#    with tf.Graph().as_default():
#        images, labels = inputs(200, 0)

#        logits = 


