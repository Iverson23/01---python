import numpy
import sys
import re


inputFilename = sys.argv[1]
file = open(inputFilename, 'r', encoding='utf-8')

coeficients = []
constants = []

letters = []
for line in file:
	split = line.split(" ");
	for k in split:
		if(k == "="):
			break
		if(k == "-"):
			continue
		if(k == "−"):
			continue
		if(k == "+"):
			continue
		if(k == ""):
			continue
		
		letter = k[-1:]
		if(letter not in letters):
			letters.append(letter)

letters.sort()

file.seek(0)
for line in file:
	equationCoeficients = []
	for letter in letters:
		equationCoeficients.append(0)
	
	split = line.split(" ");
	nextOneIsConstant = False
	nextOneIsNegative = False
	letter = None
	
	for k in split:
		if(k == ""):
			continue
		if(nextOneIsConstant):
			constants.append(int(k))
			continue
		if(k == "="):
			nextOneIsConstant = True
			continue
		if(k == "-"):
			nextOneIsNegative = True
			continue
		if(k == "−"):
			nextOneIsNegative = True
			continue
		if(k == "+"):
			continue

		
		letter = k[-1:]
		if(len(k) > 1):
			number = int(k[:-1])
		else:
			number = 1
		if(nextOneIsNegative):
			number = -number
			nextOneIsNegative = False
		
		index = letters.index(letter)
		equationCoeficients[index] = number
	
	coeficients.append(equationCoeficients)
coefArray = numpy.array(coeficients)
matrix = numpy.asmatrix(coefArray)

const2d = []
for num in constants:
	list = []
	list.append(num)
	const2d.append(list)

constArray = numpy.array(const2d)
extArray = numpy.append(coeficients, const2d, axis=1)
extendedMatrix = numpy.asmatrix(extArray)

matrixRank = numpy.linalg.matrix_rank(matrix)
extendedMatrixRank = numpy.linalg.matrix_rank(extendedMatrix)

if(matrixRank != extendedMatrixRank):
	print("no solution")
elif(matrixRank < len(letters)):
	print("solution space dimension: " + str(len(letters) - matrixRank))
else:
	result = numpy.linalg.solve(coeficients, constants)
	counter = 0
	for res in result:
		print(letters[counter] + " = " + str(res))
		counter = counter + 1
