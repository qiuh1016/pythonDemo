# coding:utf-8
"""
    手写识别系统
"""
from numpy import *
from os import listdir
import kNN


# 讲图像转为一行数组
def img2vector(filename):
    returnVect = zeros((1, 1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0, 32 * i + j] = int(lineStr[j])
    return returnVect


# 测试代码
def handwritingClassTest():
    hwLabels = []
    trainingFileList = listdir('digits/trainingDigits')
    m = len(trainingFileList)
    trainingMat = zeros((m, 1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i, :] = img2vector('digits/trainingDigits/%s' % fileNameStr)
    testFileList = listdir('digits/txt')  # testDigits
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        if fileNameStr != '.DS_Store':
            # fileStr = fileNameStr.split('.')[0]
            classNumStr = int(fileStr.split('_')[0])
            vectorUnderTest = img2vector('digits/txt/%s' % fileNameStr)   # testDigits
            classifierResult = kNN.classify0(vectorUnderTest, trainingMat, hwLabels, 3)
            print('the classifier came back with: %d, the real answer is: %d' % (classifierResult, classNumStr))
            if classifierResult != classNumStr:
                errorCount += 1.0
    print '\n the total number of errors is: %d' % errorCount
    print '\n the total error rate is: %f' % (errorCount / float(mTest))


if __name__ == '__main__':
    handwritingClassTest()
