% SStrain.m
% ===============================================
% MATLAB script that computes the fraction of amino-acids labeled as alpha helix in the training data
% ("../training_data/labels.txt") and writes the fraction to "parameters.txt".
% ===============================================
% This script contains 2 functions:
% readInput(): A function that reads in all labels from the training data and computes the fraction of alpha helices ('H')
% writeOutput(): A function that write the fraction of alpha helix in the training data to "parameters.txt"
	

inputFile = '../training_data/labels.txt';
predictionFile = 'parameters.txt';

fraction  = readInput(inputFile);
writeOutput(fraction,predictionFile);


function fraction= readInput(inputFile)
% 	Read all labels from the training data into a list, compute the fraction of all labels that are alpha helices ("H")
% 	Args: 
% 		inputFile (str): path to the input file
% 	Returns:
% 		fraction (float): fraction of all labels in inputFile that are alpha helices ("H")

    labels = "";
    fid = fopen(inputFile);
    
    while true
        name = fgetl(fid);
        seq = fgetl(fid);
        lab = fgetl(fid);
        if ~ischar(lab); break; end 
        labels= strcat(labels,lab);   
    end
    fclose(fid);
    
    helices = count(labels,'H');
    total = strlength(labels);
    fraction = helices/total;
  
end

function writeOutput(fraction,outputFile)
%   Print the fraction of all labels in the training data that are alpha helices ("H"), write the fraction to outputFile
% 	Args: 
% 		fraction (float): fraction of all labels in inputFile that are alpha helices ("H")
% 		outputFile (str): path to the output file

    sprintf("%.17f",fraction)
    fileID = fopen(outputFile, 'w');
    fprintf(fileID, "%.17f",fraction);
    fclose(fileID);

end
