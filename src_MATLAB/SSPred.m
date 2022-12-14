% SSpred.m
% ===============================================
% MATLAB script that makes a alpha-helix secondary structure prediction for a sequence file
% ===============================================
% This script contains 3 functions:
% 	readInput(): A function that reads in input from a sequence file
% 	SS_random_prediction(): A function that makes a random prediction weighted by the fraction of alpha helices in the training data
% 	writeOutput(): A function that write a prediction to an output file


inputFile = "../input_file/infile.txt";
parameters = "parameters.txt";
predictionFile = "../output_file/outfile.txt";

inputData  = readInput(inputFile);
predictions = SS_random_prediction(inputData,parameters);
writeOutput(inputData,predictions,predictionFile);

function inputData= readInput(inputFile)
% Read the input data in a FASTA format file, parse it into into a Map 
%   Args: 
%       inputFile (str): path to the input file
%   Returns:
%       inputData (map): map with format {name (str):sequence (str)} 

    inputData= containers.Map;
    
    fid = fopen(inputFile);
    while true
        name = fgetl(fid);
        seq = fgetl(fid);
        if ~ischar(seq); break; end 
        inputData(name) = seq;  
    end
    fclose(fid);
end

function randomPredictions = SS_random_prediction(inputData,parameters)
% Predict between alpha-helix (symbol: H) and non-alpha helix (symbol: -) for each amino acid in the input sequences
% The prediction is random but weighted by the overall fraction of alpha-helices in the training data (fraction stored in parameters)
% 	Args: 
% 		inputData (map): map with format {name (str):sequence (str)}
%       parameters (str): path to the file with parameters obtained from training
% 	Returns:
% 		randomPredictions (map): map with format {name (str):ss_prediction (str)} 
    
    fid = fopen(parameters);
    formatSpec = '%f';
    fraction = fscanf(fid,formatSpec);
    fclose(fid);

    keysSet = keys(inputData);
    valueSet = values(inputData);

    preds = arrayfun(@helper,valueSet,'UniformOutput', false);  
    randomPredictions = containers.Map(keysSet,preds,'UniformValues',false);
    
    function s = helper(val)
    % Helper function that reads in a string val and returns a sequence s with the same length as val
    % S is composed of 'H' and '-' chosen randomly with probablity = fraction and 1-fraction respectively    
    
        len = strlength(val);
        ss={'H', '-'};
        for i=1:len
            x=rand;
            if x<fraction
                indexes(i)= 1;
            else
                indexes(i)= 2;
            end
        end
        s = cell2mat(ss(indexes));     
    end

end

function writeOutput(inputData,predictions,predictionFile)
% Write output file with the predictions in the correct format
% 
% 	Args: 
% 		inputData (map): map with format {name (str):sequence (str)} 
% 		predictions (map): map with format {name (str):ss_prediction (str)} 
% 		outputFile (str): path to the output file

    keysSet = keys(inputData);
    fileID = fopen(predictionFile, 'w');
    for i = 1:length(keysSet)
        key= keysSet{i};
        fprintf(fileID, '%s\n%s\n%s\n', key,inputData(key),predictions(key));
    end
    fclose(fileID);
end
