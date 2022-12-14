# Script to edit if you are using Python 3 for this project. 
# Note 1: Do not change the name of this file
# Note 2: Do not change the location of this file within the BIEN410_FinalProject package
# Note 3: This file can only read in "../input_file/input_file.txt" and "parameters.txt" as input
# Note 4: This file should write output to "../output_file/outfile.txt"
# Note 5: See example of a working SSPred.py file in ../scr_Python folder

# import standard module timeit for debugging
import timeit

# define file relative paths (taken from example code)
inputFile = "../input_file/infile.txt"
parameters = "parameters.txt"
predictionFile = "../output_file/outfile.txt"

# define hyperparameters for my model
window = (5,5,5) # (0: how many residues to the left, 1: how many residues to the right, 2: orginal window size before feature selection)
# indexes of the selected features from feature selection
idx = [0, 1, 2, 3, 4, 6, 7, 8, 11, 12, 15, 16, 17, 20, 21, 22, 23, 24, 26, 27, 28, 31, 32, 35, 36, 40, 41, 42, 44, 46, 47, 48, 51, 52, 55, 56, 57, 60, 61, 62, 64, 66, 67, 68, 70, 71, 72, 74, 75, 76, 80, 81, 82, 84, 86, 87, 88, 91, 92, 95, 96, 97, 101, 102, 106, 107, 108, 110, 111, 115, 116, 117, 120, 121, 122, 124, 126, 127, 128, 131, 132, 135, 136, 137, 140, 141, 144, 147, 148, 151, 152, 155, 156, 157, 160, 161, 162, 163, 164, 166, 167, 171, 172, 175, 176, 177, 181, 184, 187, 188, 190, 191, 196, 197, 201, 202, 203, 204, 207, 208, 211, 212, 217]
useSelectedFeatures = True


# read input file (taken from example code)
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

# generate predictions based on model (modified from example code)
def SS_prediction(inputData,parameters,window,idx,useSelectedFeatures):
    '''
        Predict between alpha-helix (symbol: H) and non-alpha helix (symbol: -) for each amino acid in the input sequences
        Prediction is made by linear classification with parameters (from the parameters file) that was trained with logistric regression via gradient descent
        Args: 
            inputData (dict): dictionary with format {name (str):sequence (str)} 
            parameters (str): path to the file with with parameters obtained from training
        Returns:
            predictions (dict): dictionary with format {name (str):ss_prediction (str)} 
    '''
    
    # save parameters into a list
    params = []
    with open(parameters, 'r') as f:
        for line in f:
            params.append(float(line))
    
    # based on example code
    predictions = {}
    for name in inputData:
        seq = inputData[name]
        preds=""
        
        # modified code begins
        # convert sequence into features that my model is based on
        # and generate a prediction for each residue
        categoryVariableTemplate = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        AA = ['V','A','R','N','D','C','Q','E','G','H','I','L','K','M','F','P','S','T','W','Y']

        for r in range(len(seq)):
            # if residue is at the beginning, make it a '-'
            if r<max(window[0],window[1]):
                preds += '-'
            # if residue is at the end, also make it a '-'
            elif r>=(len(seq)-max(window[1],window[0])):
                preds += '-'
            else:
                # generate feature array for this residue
                
                residueFeatures = []
                
                # categorical variable for current residue
                local = categoryVariableTemplate.copy()
                for a in range(len(AA)):
                    if AA[a] == seq[r]:
                        local[a] = 1
                        break                
                residueFeatures.extend(local)
                
                # categorical variables for neighbor residues
                for n in range(window[2]):
                    neighbor = categoryVariableTemplate.copy()
                    for a in range(len(AA)):
                        if AA[a] == seq[r-(n+1)]:
                            neighbor[a] = 1
                            break                
                    residueFeatures.extend(neighbor)
                    neighbor = categoryVariableTemplate.copy()
                    for a in range(len(AA)):
                        if AA[a] == seq[r+(n+1)]:
                            neighbor[a] = 1
                            break                
                    residueFeatures.extend(neighbor)
                
                # keep only the selected features
                if useSelectedFeatures == True:
                    residueFeatures = [residueFeatures[i] for i in idx]
                
                # calculate the log odds of the residue being a Helix
                wx = 0
                for x in range(len(residueFeatures)):
                    wx += params[x]*residueFeatures[x]           
                odds = wx + params[-1]
                
                # assign prediction for this residue
                # if log odds is greater than 1, the residue is assigned to be a helix
                if odds>0:
                    preds += 'H'
                # else the residue is assigned as a non helix
                else:
                    preds += '-'
        
        predictions.update({name:preds})
    
    return predictions

# taken from example code
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

# modefied from example code
def main():
    start = timeit.default_timer()
    inputData = readInput(inputFile)
    predictions = SS_prediction(inputData,parameters,window,idx,useSelectedFeatures)
    writeOutput(inputData,predictions,predictionFile)
    stop = timeit.default_timer()
    print('Time: ', stop - start)

if __name__ == '__main__':
    main()