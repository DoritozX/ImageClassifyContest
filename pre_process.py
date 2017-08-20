import tensorflow as tf
import os
import re
from PIL import Image
from module_base import *
from module_tf import *

trainFileList, classes, trainDir = readAllFilesWithTag()
print("Please enter the file name of the binary data set:")
binFileName = input()
convert2bin(binFileName, trainFileList, classes, trainDir)
image, label = readDecode(binFileName)
print("Please enter number of batch size:")
batchSize = input()
image, sparseLabels = inputs(batchSize, 0)



