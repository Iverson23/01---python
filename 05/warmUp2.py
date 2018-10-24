import numpy

# 3x0 + 3x1 = 5
# 2x0 + 1x1 = 2

coeficients = []

firstEqCoef = [3,3]
secondEqCoef = [2,1]
constants = [5,2]

coeficients.append(firstEqCoef)
coeficients.append(secondEqCoef)

result = numpy.linalg.solve(coeficients, constants)
print(result)