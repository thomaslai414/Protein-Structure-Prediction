import numpy as np
import math
import timeit
import linecache
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import Lasso

start = timeit.default_timer()

# from sklearn.datasets import load_diabetes
# X,y = load_diabetes(return_X_y=True)
# features = load_diabetes()['feature_names']

# print(np.shape(X))
# print(np.shape(y))
# print(type(features))
# print(X)
# exit()

sequencesWanted = 5326 # max = 5326

inputFile  = "../training_data/labels.txt"
outputFile1 = "survivedfeaturesidx.txt"
outputFile2 = "survivedfeaturesnames.txt"
outputFile3 = "survivedfeaturesimportance.txt"

winHalfSize = 5
trainingSetSize = 1
categoryVariableTemplate = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] # numpy
AA = ['V','A','R','N','D','C','Q','E','G','H','I','L','K','M','F','P','S','T','W','Y']

beta = 0.001
threshold = 0.001
numIterations = 100

def lasso(X,y,features):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    start = timeit.default_timer()
    pipeline = Pipeline([
                         ('scaler',StandardScaler()),
                         ('model',Lasso())
    ])
    search = GridSearchCV(pipeline,
                          {'model__alpha':np.array([0.1,1,10])},
                          # {'model__alpha':np.arange(0.1,10,0.1)},
                          cv = 5, scoring="neg_mean_squared_error",# verbose=3
                          )
    search.fit(X_train,y_train)
    search.best_params_
    coefficients = search.best_estimator_.named_steps['model'].coef_
    importance = np.abs(coefficients)
#     print("Importance",importance)
    featuresSurvived = np.array(features)[importance > 0]
#     print("Features survived",featuresSurvived)
#     print("Features discarded",np.array(features)[importance == 0])
    featuresSurvivedIdx = np.nonzero(importance)[0]
    featuresSurvivedIm = importance[featuresSurvivedIdx]
    featuresSurvivedIdx = featuresSurvivedIdx.tolist()
    return featuresSurvivedIdx, featuresSurvived, featuresSurvivedIm

def createFeaturesFromFile(inputFile,winHalfSize,trainingSetSize,categoryVariableTemplate,AA,line):
    featureMatrix = [] # numpy
                     
    with open(inputFile, 'r') as f:
        for s in range(trainingSetSize):
            if line==0:
                sequence = f.readline()
                label = f.readline()
            else:
                sequence = linecache.getline(inputFile, (line-1)*3+2)
                label = linecache.getline(inputFile, (line-1)*3+3)
            
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

def writeOutput(parameters,outputFile):
    with open(outputFile, 'w') as f:
        for p in parameters:
            f.write(str(p))
            f.write('\n')
    return

def convertListToArrays(featureMatrix):
    featureMatrixNp = np.array(featureMatrix)
#     print(np.shape(featureMatrixNp))
    X = featureMatrixNp[:,:-1]
    y = featureMatrixNp[:,-1]
    return X,y

def createFeatureNames(winHalfSize,AA):
    features = []
    for aa in AA:
        features.append(aa+"0")
    
    for n in range(winHalfSize):
        nminus = (n+1)*-1
        nplus = (n+1)
        for aa in AA:
            features.append(aa+str(nminus))
        for aa in AA:
            features.append(aa+str(nplus))
    
    return features

features = createFeatureNames(winHalfSize,AA)
print(type(features))
print(len(features))
print(features)
exit()

def main():
#     start = timeit.default_timer()
#     line = 1
#     featureMatrix = createFeaturesFromFile(inputFile,winHalfSize,trainingSetSize,categoryVariableTemplate,AA,line)
#     print(featureMatrix) # Debug
#     stop = timeit.default_timer()
#     print('Time for data mapping: ', stop - start)    
#     print(len(featureMatrix))
#     print(len(featureMatrix[0]))
#     start = timeit.default_timer()     
#     X,y = convertListToArrays(featureMatrix)
#     print(np.shape(X))
#     print(np.shape(y))
#     features = createFeatureNames(winHalfSize,AA)
#     featuresSurvivedIdx, featuresSurvived, featuresSurvivedIm = lasso(X,y,features)
#     print(featuresSurvivedIdx)
#     print(type(featuresSurvivedIdx))
#     stop = timeit.default_timer()
#     print('Time for feature selection: ', stop - start)       
    
    featuresSurvivedIdxs = []
    featuresSurviveds = []
    featuresSurvivedIms = []
    
    for s in range(sequencesWanted):
        featureMatrix = createFeaturesFromFile(inputFile,winHalfSize,trainingSetSize,categoryVariableTemplate,AA,s+1)
        X,y = convertListToArrays(featureMatrix)
        features = createFeatureNames(winHalfSize,AA)
        featuresSurvivedIdx, featuresSurvived, featuresSurvivedIm = lasso(X,y,features)
        featuresSurvivedIdxs.extend(featuresSurvivedIdx)
        featuresSurviveds.extend(featuresSurvived)
        featuresSurvivedIms.extend(featuresSurvivedIm)
    
    writeOutput(featuresSurvivedIdxs,outputFile1)
    writeOutput(featuresSurviveds,outputFile2)
    writeOutput(featuresSurvivedIms,outputFile3)

if __name__ == '__main__':
    main()
    stop = timeit.default_timer()
    print('Time lapsed: ', stop - start)   