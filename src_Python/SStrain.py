'''
SStrain.py
===================================================
Python script that computes the fraction of amino-acids labeled as alpha helix in the training data
("../training_data/labels.txt") and writes the fraction to "parameters.txt".
===================================================
This script contains 2 functions:
    readInput(): A function that reads in all labels from the training data and computes the fraction of alpha helices ('H')
    writeOutput(): A function that write the fraction of alpha helix in the training data to "parameters.txt"
'''

inputFile  = "../training_data/labels.txt"
outputFile = "parameters.txt"

def readInput(inputFile):
    '''
        Read all labels from the training data into a list, compute the fraction of all labels that are alpha helices ("H")
        Args: 
            inputFile (str): path to the input file
        Returns:
            fraction (float): fraction of all labels in inputFile that are alpha helices ("H")
    '''
    labels = []
    with open(inputFile, 'r') as f:
        while True:
            name = f.readline()
            sequence = f.readline()
            label = f.readline()
            if not label: break
            labels=labels+[x for x in label.rstrip()]

        helices= labels.count("H")
        total =len(labels)
        fraction = helices/total
        
    return fraction

def writeOutput(fraction,outputFile):
    '''
        Print the fraction of all labels in the training data that are alpha helices ("H"), write the fraction to outputFile
        Args: 
            fraction (float): fraction of all labels in inputFile that are alpha helices ("H")
            outputFile (str): path to the output file
    '''
    print(fraction)
    with open(outputFile, 'w') as f:
        f.write(str(fraction))
    return

def main():

    fraction = readInput(inputFile)
    writeOutput(fraction,outputFile)
    
if __name__ == '__main__':
    main()


