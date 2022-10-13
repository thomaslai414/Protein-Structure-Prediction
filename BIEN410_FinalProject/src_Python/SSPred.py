'''
SSpred.py
===================================================
Python script that makes a alpha-helix secondary structure prediction for a sequence file
===================================================
This script contains 3 functions:
    readInput(): A function that reads in input from a sequence file
    SS_random_prediction(): A function that makes a random prediction weighted by the fraction of alpha helices in the training data
    writeOutput(): A function that write a prediction to an output file
'''

import random

inputFile 		= "../input_file/infile.txt"
parameters 		= "parameters.txt"
predictionFile	= "../output_file/outfile.txt"

def readInput(inputFile):
    '''
        Read the data in a FASTA format file, parse it into into a python dictionnary 
        Args: 
            inputFile (str): path to the input file
        Returns:
            training_data (dict): dictionary with format {name (str):sequence (str)} 
    '''
    inputData = {}
    with open(inputFile, 'r') as f:
        while True:
            name = f.readline()
            seq = f.readline()
            if not seq: break
            inputData.update({name.rstrip():seq.rstrip()})
    
    return inputData

def SS_random_prediction(inputData,parameters):
    '''
        Predict between alpha-helix (symbol: H) and non-alpha helix (symbol: -) for each amino acid in the input sequences
        The prediction is random but weighted by the overall fraction of alpha helices in the training data (stored in parameters)
        Args: 
            inputData (dict): dictionary with format {name (str):sequence (str)} 
            parameters (str): path to the file with with parameters obtained from training
        Returns:
            randomPredictions (dict): dictionary with format {name (str):ss_prediction (str)} 
    '''

    with open(parameters, 'r') as f:
        fraction = float(next(f))
    
    randomPredictions = {}
    for name in inputData:
        seq = inputData[name]
        preds=""
    
        for aa in seq:
            preds=preds+random.choices(["H","-"], weights = [fraction,1-fraction])[0]
        
        randomPredictions.update({name:preds})
    
    return randomPredictions

def writeOutput(inputData,predictions,outputFile):
    '''
        Writes output file with the predictions in the correct format
        Args: 
            inputData (dict): dictionary with format {name (str):sequence (str)} 
            predictions (dict): dictionary with format {name (str):ss_prediction (str)} 
            outputFile (str): path to the output file
    '''
    with open(outputFile, 'w') as f:
        for name in inputData:
            f.write(name+"\n")
            f.write(inputData[name]+"\n")
            f.write(predictions[name]+"\n")

    return


def main():

    inputData = readInput(inputFile)
    predictions = SS_random_prediction(inputData,parameters)
    writeOutput(inputData,predictions,predictionFile)

if __name__ == '__main__':
    main()


