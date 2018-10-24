import numpy


numbersList = []

listofNumbers = [1,2,3]
secondListofNumbers = [4,5,6]
thirdListofNumbers = [7,8,9]

numbersList.append(listofNumbers)
numbersList.append(secondListofNumbers)
numbersList.append(thirdListofNumbers)

npArray = numpy.array(numbersList)
matrix = numpy.asmatrix(npArray)
print("matrix: \n" + str(matrix))
det = numpy.linalg.det(npArray)
print("determinant: " + str(det))
rank = numpy.linalg.matrix_rank(matrix)
print("rank: " + str(rank))
matrixInv = numpy.linalg.inv(matrix)
print("inverted matrix: \n" + str(matrixInv))