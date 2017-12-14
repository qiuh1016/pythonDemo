from numpy import *
import re


def loadDataSet():
    postingList = [
        ['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
        ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
        ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
        ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
        ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
        ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']
    ]
    classVec = [0, 1, 0, 1, 0, 1]  # 1 is abusive, 0 not
    return postingList, classVec


def createVocabList(inputDataSet):
    vocabSet = set([])
    for document in inputDataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)


def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print 'the word: %d is not in my vocabulary'
    return returnVec


def bagOfWords2Vec(vocabList, inputSet):
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
        else:
            print 'the word: %d is not in my vocabulary'
    return returnVec


def trainNB0(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory) / float(numTrainDocs)
    p0Num = ones(numWords)
    p1Num = ones(numWords)
    p0Denom = 2.0
    p1Denom = 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p0Vect = log(p0Num / p0Denom)
    p1Vect = log(p1Num / p1Denom)
    return p0Vect, p1Vect, pAbusive


def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    return 1 if p1 > p0 else 0


def testingNB():
    listOPosts, listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts)
    trainMat = []
    for postingDocs in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList, postingDocs))
    p0V, p1V, pAb = trainNB0(trainMat, array(listClasses))

    testEntry = ['love', 'my', 'dalmation']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print testEntry, 'classify as: ', classifyNB(thisDoc, p0V, p1V, pAb)
    testEntry = ['stupid', 'garbage']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print testEntry, 'classify as: ', classifyNB(thisDoc, p0V, p1V, pAb)

    print p0V


if __name__ == '__main__':
    # pList, vec = loadDataSet()
    #
    # myVocabList = createVocabList(pList)
    # trainMat = []
    # for p in pList:
    #     trainMat.append(setOfWords2Vec(myVocabList, p))
    #
    # p0Vect, p1Vect, pAbusive = trainNB0(trainMat, vec)
    #
    # # print p0Vect

    # testingNB()

    # mySent = 'This book is the best book on Python or M.L. I have ever laid eyes upon.'
    regEx = re.compile('\\W*')
    # listOfTokens = regEx.split(mySent)
    # newList = [tok.lower() for tok in listOfTokens if len(tok) > 0]
    # print newList

    emailText = open('email/ham/6.txt').read()
    listOfTokens = regEx.split(emailText)
    newList = [tok.lower() for tok in listOfTokens if len(tok) > 0]
    print newList
