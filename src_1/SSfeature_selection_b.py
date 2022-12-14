import matplotlib.pyplot as plt
import numpy as np

inputFile1 = "survivedfeaturesidx.txt"
inputFile2 = "survivedfeaturesnames.txt"
inputFile3 = "survivedfeaturesimportance.txt"

winHalfSize = 5
AA = ['V','A','R','N','D','C','Q','E','G','H','I','L','K','M','F','P','S','T','W','Y']

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

def readInput(fileName):
    data = []
    with open(fileName, 'r') as f:
        for line in f:
            data.append(float(line))
    
    return data

def readInput2(fileName):
    data = []
    with open(fileName, 'r') as f:
        for line in f:
            data.append(line.rstrip())
    
    return data

def writeOutput(parameters,outputFile):
    with open(outputFile, 'w') as f:
        for p in parameters:
            f.write(str(p))
            f.write('\n')
    return

featureNames = createFeatureNames(winHalfSize,AA)
idx = readInput(inputFile1)
names = readInput2(inputFile2)
importance = readInput(inputFile3)

featureScore = [0]*len(featureNames)

for f in range(len(featureNames)):
    for h in range(len(names)):
        if names[h]==featureNames[f]:
            featureScore[f]+=importance[h]

# print(featureScore)

FS = np.array(featureScore)

plt.plot(FS)
# plt.show()
# print(FS)

print(np.size(FS),"features have accumulated importance > 0")

FS_5_idx = np.argwhere(FS>=0.5)

FS_5_inv_idx = np.argwhere(FS<0.5)
FS_5 = FS.copy()
FS_5[FS_5_inv_idx] = 0

plt.plot(FS_5)
# plt.show()

# print(FS_5_idx)
# print(FS_5)

print(np.size(FS_5_idx),"features have accumulated importance > 0.5")

outputFile1 = "fs5idx.txt"
outputFile2 = "fs10idx.txt"
outputFile3 = "fs20idx.txt"
outputFile4 = "fs40idx.txt"

writeOutput([FS_5_idx.reshape(-1).tolist()],outputFile1)

FS_10_idx = np.argwhere(FS>=1)

FS_10_inv_idx = np.argwhere(FS<1)
FS_10 = FS.copy()
FS_10[FS_10_inv_idx] = 0

plt.plot(FS_10)
# plt.show()

print(np.size(FS_10_idx),"features have accumulated importance > 1")

writeOutput([FS_10_idx.reshape(-1).tolist()],outputFile2)

FS_20_idx = np.argwhere(FS>=2)

FS_20_inv_idx = np.argwhere(FS<2)
FS_20 = FS.copy()
FS_20[FS_20_inv_idx] = 0

plt.plot(FS_20)
# plt.show()

print(np.size(FS_20_idx),"features have accumulated importance > 2")

writeOutput([FS_20_idx.reshape(-1).tolist()],outputFile3)

FS_40_idx = np.argwhere(FS>=4)

FS_40_inv_idx = np.argwhere(FS<4)
FS_40 = FS.copy()
FS_40[FS_40_inv_idx] = 0

plt.plot(FS_40)
# plt.show()

print(np.size(FS_40_idx),"features have accumulated importance > 4")

writeOutput([FS_40_idx.reshape(-1).tolist()],outputFile4)

FS_15_idx = np.argwhere(FS>=1.5)

FS_15_inv_idx = np.argwhere(FS<1.5)
FS_15 = FS.copy()
FS_15[FS_15_inv_idx] = 0

# plt.plot(FS_15)
# plt.show()

print(np.size(FS_15_idx),"features have accumulated importance > 1.5")

writeOutput([FS_15_idx.reshape(-1).tolist()],"fs15idx.txt")

# print(featureScore[0:3])
# print(len(featureScore))
# print(type(featureScore))
# print(featureNames[0:10])
# print(idx[0:10])
# print(names[0:10])
# print(importance[0:10])
# print(len(idx))
# print(type(idx))
