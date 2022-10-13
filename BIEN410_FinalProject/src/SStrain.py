'''
0 valine - val - V
1 alanine - ala - A 
2 arginine - arg - R 
3 asparagine - asn - N 
4 aspartic acid - asp - D 
5 cysteine - cys - C 
6 glutamine - gln - Q 
7 glutamic acid - glu - E 
8 glycine - gly - G 
9 histidine - his - H 
10 isoleucine - ile - I 
11 leucine - leu - L 
12 lysine - lys - K 
13 methionine - met - M 
14 phenylalanine - phe - F 
15 proline - pro - P 
16 serine - ser - S 
17 threonine - thr - T 
18 tryptophan - trp - W 
19 tyrosine - tyr - Y

Whole training set = 5326 sequences

'''

import numpy as np
import math
import timeit

inputFile  = "../training_data/labels.txt"
outputFile = "parameters.txt"

winHalfSize = 5
trainingSetSize = 3800
categoryVariableTemplate = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] # numpy
AA = ['V','A','R','N','D','C','Q','E','G','H','I','L','K','M','F','P','S','T','W','Y']

beta = 0.00001
threshold = 1
numIterations = 50

idx = [0, 1, 2, 3, 4, 6, 7, 8, 11, 12, 15, 16, 17, 20, 21, 22, 23, 24, 26, 27, 28, 31, 32, 35, 36, 40, 41, 42, 44, 46, 47, 48, 51, 52, 55, 56, 57, 60, 61, 62, 64, 66, 67, 68, 70, 71, 72, 74, 75, 76, 80, 81, 82, 84, 86, 87, 88, 91, 92, 95, 96, 97, 101, 102, 106, 107, 108, 110, 111, 115, 116, 117, 120, 121, 122, 124, 126, 127, 128, 131, 132, 135, 136, 137, 140, 141, 144, 147, 148, 151, 152, 155, 156, 157, 160, 161, 162, 163, 164, 166, 167, 171, 172, 175, 176, 177, 181, 184, 187, 188, 190, 191, 196, 197, 201, 202, 203, 204, 207, 208, 211, 212, 217]
useSelectedFeatures = False

def createFeaturesFromFile(inputFile,winHalfSize,trainingSetSize,categoryVariableTemplate,AA):
    featureMatrix = [] # numpy
                     
    with open(inputFile, 'r') as f:
        for s in range(trainingSetSize):
            name = f.readline()
            sequence = f.readline()
            label = f.readline()
            
            sequenceFeatureMatrix = [] # numpy
            
            for r in range(len(sequence)):
                if r<winHalfSize:
                    continue
                elif r>=(len(sequence)-winHalfSize):
                    continue
                else:
                    residueFeatures = [] # numpy
                    
                    local = categoryVariableTemplate.copy() # numpy
                    for a in range(len(AA)):
                        if AA[a] == sequence[r]:
                            local[a] = 1
                            break                
                    residueFeatures.extend(local) # numpy
                    
                    for n in range(winHalfSize):
                        neighbor = categoryVariableTemplate.copy() # numpy
                        for a in range(len(AA)):
                            if AA[a] == sequence[r-(n+1)]:
                                neighbor[a] = 1
                                break                
                        residueFeatures.extend(neighbor) # numpy
                        neighbor = categoryVariableTemplate.copy() # numpy
                        for a in range(len(AA)):
                            if AA[a] == sequence[r+(n+1)]:
                                neighbor[a] = 1
                                break                
                        residueFeatures.extend(neighbor) # numpy
                    
                    if label[r]=='H':
                        residueFeatures.append(1)
                    else:
                        residueFeatures.append(0)
                    
                    sequenceFeatureMatrix.append(residueFeatures)            
            featureMatrix.extend(sequenceFeatureMatrix)
    
    return featureMatrix
 
def logisticRegression(featureMatrix,beta,threshold,numIterations,mode):
    parameters = [0] * len(featureMatrix[0])

# Terminating Criteria -> Threshold
    if mode==0:
        it = 0
        while True:
            w_incrs = [0] * (len(parameters)-1)
            b_incr = 0
            
            for sample in featureMatrix:
    #             print(sample)
    #             print(all(isinstance(x,int) for x in sample))
    #             exit()

                y_prime = 2*sample[-1]-1
                alpha_0 = 0
                
                for j in range(len(parameters)-1):
                    alpha_0 += parameters[j]*sample[j]
                    
                alpha = y_prime*(alpha_0+parameters[-1])
                incr = y_prime/(1+math.exp(alpha))
                
                b_incr += incr
                for w in range(len(w_incrs)):
                    w_incrs[w] += incr*sample[w]
            
            parameters[-1] += beta*b_incr
            for w in range(len(parameters)-1):
                parameters[w] += beta*w_incrs[w]
            
            it += 1
            if (all(w_incr<threshold for w_incr in w_incrs) and b_incr<threshold):
                print('Number of GD iterations: ',it)
                break

# Terminating Criteria -> number of iterations
    elif mode==1:
        it = 0
        while True:
            w_incrs = [0] * (len(parameters)-1)
            b_incr = 0
            
            for sample in featureMatrix:
    #             print(sample)
    #             print(all(isinstance(x,int) for x in sample))
    #             exit()

                y_prime = 2*sample[-1]-1
                alpha_0 = 0
                
                for j in range(len(parameters)-1):
                    alpha_0 += parameters[j]*sample[j]
                    
                alpha = y_prime*(alpha_0+parameters[-1])
                try:
                    incr = y_prime/(1+math.exp(alpha))
                except OverflowError:
                    incr = 0
                
                b_incr += incr
                for w in range(len(w_incrs)):
                    w_incrs[w] += incr*sample[w]
            
            parameters[-1] += beta*b_incr
            for w in range(len(parameters)-1):
                parameters[w] += beta*w_incrs[w]
            
            it += 1
            if it==numIterations: break
        
    return parameters

def writeOutput(parameters,outputFile):
    with open(outputFile, 'w') as f:
        for p in parameters:
            f.write(str(p))
            f.write('\n')
    return

def applyFeaturesSelected(featureMatrix,idx):
    featureOnlyMatrix = []
    idx.append(220)
    for sequence in featureMatrix:
        featureOnlyMatrix.append([sequence[i] for i in idx])
    return featureOnlyMatrix

def main():
#     featureMatrix = createFeaturesFromFile(inputFile,winHalfSize,trainingSetSize,categoryVariableTemplate,AA)
#     print(len(featureMatrix))
#     print(len(featureMatrix[0]))
#     featureOnlyMatrix = applyFeaturesSelected(featureMatrix,idx)
#     print(featureOnlyMatrix)
#     print(len(featureOnlyMatrix))
#     print(len(featureOnlyMatrix[0]))
#     print([seq[1] for seq in featureMatrix])
#     print([seq[0] for seq in featureOnlyMatrix])
#     print([seq[28] for seq in featureMatrix])
#     print([seq[7] for seq in featureOnlyMatrix])
#     print([seq[220] for seq in featureMatrix])
#     print([seq[30] for seq in featureOnlyMatrix])
#     exit()
    
    if useSelectedFeatures == True:
        start = timeit.default_timer()
        featureMatrix = createFeaturesFromFile(inputFile,winHalfSize,trainingSetSize,categoryVariableTemplate,AA)
        featureOnlyMatrix = applyFeaturesSelected(featureMatrix,idx)
        stop = timeit.default_timer()
        print('Lap 1: ', stop - start)
        start = timeit.default_timer()
        parameters = logisticRegression(featureOnlyMatrix,beta,threshold,numIterations,1)
        stop = timeit.default_timer()
        print('Lap 2: ', stop - start)
        writeOutput(parameters,outputFile)
    
    else:
        start = timeit.default_timer()
        featureMatrix = createFeaturesFromFile(inputFile,winHalfSize,trainingSetSize,categoryVariableTemplate,AA)
    #     print(featureMatrix) # Debug
        stop = timeit.default_timer()
        print('Lap 1: ', stop - start)
        start = timeit.default_timer()
        parameters = logisticRegression(featureMatrix,beta,threshold,numIterations,1)
        stop = timeit.default_timer()
        print('Lap 2: ', stop - start)
    #     print(parameters) # Debug
    #     print(len(parameters)) # Debug
        writeOutput(parameters,outputFile)
    
if __name__ == '__main__':
    main()