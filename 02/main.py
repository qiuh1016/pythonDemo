# print '123'
# a = 1
# while a == 1:
#     print(1)


# numbers = [12, 37, 5, 42, 8, 3]
# even = []
# odd = []
#
# while len(numbers) > 0:
#     number = numbers.pop()
#     if number % 2 == 0:
#         even.append(number)
#     else:
#         odd.append(number)
#
# print(even)
# print(odd)

# import numpy
# randomMat = numpy.mat(numpy.random.rand(4, 4))
# invRandomMat = randomMat.I
# print invRandomMat * randomMat

from numpy import *
randomMat = mat(random.rand(4, 4))
invRandomMat = randomMat.I
print invRandomMat * randomMat
