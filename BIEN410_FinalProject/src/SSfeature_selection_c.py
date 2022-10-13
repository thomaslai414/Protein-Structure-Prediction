def writeOutput(parameters,outputFile):
    with open(outputFile, 'w') as f:
        for p in parameters:
            f.write(str(p))
            f.write('\n')
    return

feature80 = []

for i in range(0,60):
    feature80.append(i)
    
for i in range(80,100):
    feature80.append(i)

writeOutput([feature80],'fs80idx.txt')

feature60 = [1, 2, 4, 7, 8, 11, 12, 15, 21, 22, 24, 27, 28, 31, 35, 41, 42, 44, 46, 47, 48, 51, 52, 55, 61, 67, 68, 71, 81, 82, 84, 86, 87, 88, 91, 92, 95, 101, 107, 108, 111, 120, 121, 122, 131, 132, 135, 141, 147, 161, 162, 167, 171, 172, 181, 184, 201, 207, 211, 212]
feature123 = [0, 1, 2, 3, 4, 6, 7, 8, 11, 12, 15, 16, 17, 20, 21, 22, 23, 24, 26, 27, 28, 31, 32, 35, 36, 40, 41, 42, 44, 46, 47, 48, 51, 52, 55, 56, 57, 60, 61, 62, 64, 66, 67, 68, 70, 71, 72, 74, 75, 76, 80, 81, 82, 84, 86, 87, 88, 91, 92, 95, 96, 97, 101, 102, 106, 107, 108, 110, 111, 115, 116, 117, 120, 121, 122, 124, 126, 127, 128, 131, 132, 135, 136, 137, 140, 141, 144, 147, 148, 151, 152, 155, 156, 157, 160, 161, 162, 163, 164, 166, 167, 171, 172, 175, 176, 177, 181, 184, 187, 188, 190, 191, 196, 197, 201, 202, 203, 204, 207, 208, 211, 212, 217]

feature80hb60 = []

for i in range(0,220):
    if any([j==i for  j in feature60]) or any([k==i for k in feature80]):
        feature80hb60.append(i)

print('# of 80hb60: ',len(feature80hb60))
writeOutput([feature80hb60],'fs80hb60idx.txt')

feature80hb123 = []

for i in range(0,220):
    if any([j==i for  j in feature123]) or any([k==i for k in feature80]):
        feature80hb123.append(i)

print('# of 80hb123: ',len(feature80hb123))
writeOutput([feature80hb123],'fs80hb123idx.txt')