from numpy import *


def loadDataSet():
    dataMat = []
    labelMat = []
    fs = open('txt/testSet.txt')
    for line in fs.readlines():
        lineArr = line.strip().split()
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
        labelMat.append(int(lineArr[2]))
    return dataMat, labelMat


def sigmoid(z):
    return 1.0 / (1 + exp(-z))


def gradAscent(dataMatIn, classLabels):
    dataMatrix = mat(dataMatIn)
    labelMatrix = mat(classLabels).transpose()
    m, n = shape(dataMatrix)
    alpha = 0.001
    maxCycles = 500
    weights = ones((n, 1))
    for k in range(maxCycles):
        h = sigmoid(dataMatrix * weights)
        error = labelMatrix - h
        weights = weights + alpha * dataMatrix.transpose() * error
    return weights


if __name__ == '__main__':
    dataMat, labelMat = loadDataSet()
    print gradAscent(dataMat, labelMat)
