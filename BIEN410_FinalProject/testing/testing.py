"""
testing.py
===================================================
Script to test your secondary structure predictions
===================================================
"""

import argparse
import os.path
import re
import warnings

def check_file_format( path ):
    """
    Checks the format of the file path
    Args: 
        path (str): path a file
    """

    if not os.path.exists(path):
        raise FileNotFoundError('Input file does not exist: '+ path)

    with open( path ) as fh:
        while True:
            name = fh.readline()
            seq = fh.readline()
            struct = fh.readline()
            if not struct: break
            
            pattern1 = re.compile("^>d.+\|.+\n")
            pattern2 = re.compile("^[A-Z]+\n")
            pattern3 = re.compile("^[H\-]+\n")
            matched1 = bool(re.match(pattern1, name))
            matched2 = bool(re.match(pattern2, seq))
            matched3 = bool(re.match(pattern3, struct))
            
            if not matched1:
                raise UserWarning('Format of the description line may be wrong for file '+ path+ "\nCorrect format example: '>d1dlwa | 116'")
            if not matched2:
                raise UserWarning('Format of the sequence line may be wrong for file '+ path+ "\nCorrect format example: 'SLFEQLGGQAAVQA'")
            if not matched3:
                raise UserWarning('Format of the secondary structure line may be wrong for file '+ path+ "\nCorrect format example: '--H-HH-H--H-H--'")
                    
        return

def read_fasta ( path ):
    """
    Reads the file path into a dictionary and check file format
    Args: 
        path (str): path a file
    Returns:
        fdict (dict): dictionary with format {name (str):ss_prediction (str)} or {name (str):ss_labels (str)} 
    """

    fdict = {}
    
    check_file_format(path)

    with open( path ) as fh:
        while True:
            name = fh.readline()
            seq = fh.readline()
            struct = fh.readline()
            if not struct: break
            fdict[name.rstrip()]=struct.rstrip()
    return fdict

def compute_prediction_accuracy(preds,correct,output):
    """
    Computes prediction accuracy by comparing the preds and the correct dictonnaries.
    Prints the accuracy to stdout or to output
    Args: 
            preds (dict): dictionary with format {name (str):ss_prediction (str)}
            correct (dict): dictionary with format {name (str):ss_labels (str)} 
            output (str): path to the output file
    """

    if not set(preds.keys()) == set(correct.keys()):
        raise UserWarning('Format of the description line cannot be matched between predictions file and labels file')

    total,correct_pred,incorrect_pred=0,0,0
    for name in preds:
        p = preds[name]
        c = correct[name]
        if len(p) != len(c):
            raise UserWarning('Different lengths between secondary structure predictions and secondary structure labels')
        total=total+len(p)
        correct_pred=correct_pred+sum(c1==c2 for c1,c2 in zip(p,c))
        incorrect_pred=incorrect_pred+sum(c1!=c2 for c1,c2 in zip(p,c))

    accuracy = correct_pred/total*100

    if output == None:
        print("Prediction accuracy: ", (accuracy),"%")
    else:
        with open( output,"w" ) as fh:
            fh.write(str(accuracy))
    return
    
def main ( ):

    # Argument parsing 
    parser = argparse.ArgumentParser(description='Script to evaluate the accuracy of a secondary structure prediction.')
    parser.add_argument( "-p", '--predictions', help='Path to the file containing the secondary structure prediction to evaluate.' )
    parser.add_argument( "-l", '--labels', help='Path to the correct secondary structure labelling.' )
    parser.add_argument( "-o", '--output', default=None, help='Output file (Optional, default stdout).' )
    args = parser.parse_args()

    # Load the correct and prediction files
    preds= read_fasta(args.predictions)
    correct= read_fasta(args.labels)

    # Get the prediction accuracy
    compute_prediction_accuracy(preds,correct,args.output)

if __name__ == "__main__":
    main( )


