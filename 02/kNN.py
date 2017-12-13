# coding:utf-8
from numpy import *
import operator
import matplotlib
import matplotlib.pyplot as plt


def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels


# 通过KNN进行分类
def classify(input, dataSet, label, k):
    data_size = dataSet.shape[0]
    # 计算欧式距离
    diff = tile(input, (data_size, 1)) - dataSet
    sq_diff = diff ** 2
    square_dist = sum(sq_diff, axis=1)  # 行向量分别相加，从而得到新的一个行向量
    dist = square_dist ** 0.5

    # 对距离进行排序
    sorted_dist_index = argsort(dist)  # argsort()根据元素的值从小到大对元素进行排序，返回下标

    class_count = {}
    for i in range(k):
        vote_label = label[sorted_dist_index[i]]
        # 对选取的K个样本所属的类别个数进行统计
        class_count[vote_label] = class_count.get(vote_label, 0) + 1

    # 选取出现的类别次数最多的类别
    max_count = 0
    for key, value in class_count.items():
        if value > max_count:
            max_count = value
            classes = key

    return classes


# 通过KNN进行分类
def classify0(inX, dataSet, labels, k):  # inX为用于分类的输入向量，dataSet为输入的训练样本集， labels为训练标签，k表示用于选择最近的数目
    dataSetSize = dataSet.shape[0]  # dataSet的行数
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet  # 将inX数组复制成与dataSet相同行数，与dataSet相减，求坐标差
    sqDiffMat = diffMat ** 2  # diffMat的平方
    sqDistances = sqDiffMat.sum(axis=1)  # 将sqDiffMat每一行的所有数相加
    distances = sqDistances ** 0.5  # 开根号，求点和点之间的欧式距离
    sortedDistIndicies = distances.argsort()  # 将distances中的元素从小到大排列，提取其对应的index，然后输出到sortedDistIndicies
    classCount = {}  # 创建字典
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]  # 前k个标签数据
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1  # 判断classCount中有没有对应的voteIlabel，
        # 如果有返回voteIlabel对应的值，如果没有则返回0，在最后加1。为了计算k个标签的类别数量
    sortedClassCount = sorted(classCount.items(),
                              key=operator.itemgetter(1), reverse=True)  # 生成classCount的迭代器，进行排序，
    # operator.itemgetter(1)以标签的个数降序排序
    return sortedClassCount[0][0]  # 返回个数最多的标签


# 将文本文件转换到numpy
def file2matrix(filename, split, number):
    fr = open(filename)
    arrayOLines = fr.readlines()  # 读入所有行
    numberOfLines = len(arrayOLines)  # 行数
    returnMat = zeros((numberOfLines, number))  # 创建数组，数据集
    classLabelVector = []  # 标签集
    index = 0
    for line in arrayOLines:
        line = line.strip()  # 移除所有的回车符
        listFromLine = line.split(split)  # 把一个字符串按,分割成字符串数组
        returnMat[index, :] = listFromLine[0: number]  # 取listFromLine的前三个元素放入returnMat
        classLabelVector.append(int(listFromLine[-1]))  # 选取listFromLine的最后一个元素依次存入classLabelVector列表中
        index += 1
    return returnMat, classLabelVector


# 归一化特征值
def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m, 1))
    normDataSet = normDataSet / tile(ranges, (m, 1))  # element wise divide
    return normDataSet, ranges, minVals


# 测试代码
def datingClassTest():
    hoRatio = 0.10
    datingDataMat, datingLabels = file2matrix('datingTestSet.txt', '\t', 3)
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m * hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify(normMat[i, :], normMat[numTestVecs:m, :], datingLabels[numTestVecs:m], 3)
        print "the classifier came back with: %d, the real answer is: %d" % (classifierResult, datingLabels[i])
        if (classifierResult != datingLabels[i]): errorCount += 1.0
    print "the total error rate is: %f" % (errorCount / float(numTestVecs))
    print errorCount


# 预测函数
def classifyPerson():
    resultList = ['not at all', 'in small doses', 'in large doses']
    percentTats = float(raw_input('percetage of time spent playing video games?'))
    ffMiles = float(raw_input('fraquent fliter miles earned per year?'))
    iceCream = float(raw_input('liters of iceCream consumed per year?'))
    datingDataMat, datingLabels = file2matrix('datingTestSet.txt', '\t', 3)
    normMat, ranges, minVals = autoNorm(datingDataMat)
    inArr = array([ffMiles, percentTats, iceCream])
    classifierResult = classify((inArr - minVals) / ranges, normMat, datingLabels, 3)
    print("You will probably like this person:", resultList[classifierResult - 1])


# classifyPerson()

# datingDataMat为特征数据集，datingLabels为标签集
# datingDataMat, datingLabels = file2matrix('datingTestSet.txt')
# normDataSet, ranges, minVals = autoNorm(datingDataMat)
#
# fig = plt.figure()
# ax = fig.add_subplot(111)  # 一行一列一个
# ax.scatter(normDataSet[:, 1], normDataSet[:, 2], 15.0 * array(datingLabels), 15.0 * array(datingLabels))
# # scatter画散点图，使用标签属性绘制不同颜色不同大小的点
# plt.show()


group, labels = createDataSet()
print classify([0, 0], group, labels, 3)


# datingDataMat, datingLabels = file2matrix('data.txt', ',', 2)
# autoNorm(datingDataMat)


'''
    手写识别系统
'''
def img2vector(filename):
    returnVect = zeros((1, 1024))
    
'''
    手写识别系统 结束
'''
