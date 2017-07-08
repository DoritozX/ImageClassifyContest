##-*- coding:utf8*-
import tensorflow as tf
import os
import re
from PIL import Image
from module import *

def convert2bin(binFileName):
    """
    convert the training files int binary format
    binFileName: "xxxx.tfrecords"
    """
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
    #convert to the binary file
    writer = tf.python_io.TFRecordWriter(binFileName)

    for index, fileName in enumerate(trainFileList):
        absPath = trainDir + '\\' + fileName
        img = Image.open(absPath)
        img = img.resize((128, 128))
        img_binary = img.tobytes()
        example = tf.train.Example(features = tf.train.Features(feature = {"label": tf.train.Feature(int64_list = tf.train.Int64List(value = [classes[index]])),\
                                                                           "img_raw": tf.train.Feature(bytes_list = tf.train.BytesList(value = [img_binary]))}))
        writer.write(example.SerializeToString())
        print(fileName, " has been read...")

    writer.close()
    return

def readDecode(binFileName):
    reader = tf.TFRecordReader()
    serializedExample = reader.read(binFileName)
    features = tf.parse_single_example(serializedExample,\
                                       features = {"label": tf.FixedLenFeature([], tf.int64),\
                                                   "img_raw": tf.FixedLenFeature([], tf.string)})
    image = tf.decode_raw(features["img_raw", tf.uint8])
    tf.reshape(image, [224,224,3])
    image = tf.cast(image, tf.float32) * (1./255) - 0.5
    label = tf.cast(features['label'], tf.int32)

    return image, label
    