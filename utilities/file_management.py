from utilities.constants import *
import os
import csv
import pandas as pd

def get_ids(file,delimiter='\t'):
    """Gets only the id strings of the selected Database (csv file)

    Args:
        file: file name as a relative path from DATA_FOLDER

    Kwargs:
        delimiter: separator for values in the csvfile

    Return:
        ids: iterable list of all the id strings

    """
    ids = []

    #where the file is stored (absolute path)
    file = os.path.join(DATA_FOLDER,file)

    with open(file) as csvfile:
        reader = csv.reader(csvfile, delimiter = delimiter)
        for sound in reader:
            ids.append(sound[0])
        ids.remove("recordingmbid")

    return ids

def load_file(file,sep='\t',index_col=0,sort = True):
    """Loads file into a pandas dataframe

    Args:
        file: file name as a relative path from DATA_FOLDER
    
    Kwargs:
        sep: separator for values in csvfile for pandas' read_csv (default: '\t')
        index_col: column that will be the index in the pandas' dataframe object (default: 0)
        sort: if the dataframe is to be sorted by index (default: True)

    Return:
        df: dataframe from CSV

    """

    file = os.path.join(DATA_FOLDER,file) 
    with open(file) as tsvfile:
        df = pd.read_csv(file,sep=sep,index_col=index_col,low_memory = False)
    
    if sort: df = df.sort_index()
    
    return df

def save_file(df,file,sep='\t'):
    """Saves the dataframe as csv

    Args:
        file: file name as a relative path from DATA_FOLDER
    
    Kwargs:
        sep: separator for values in csvfile for pandas' to_csv (default: '\t')

    Return:
        df: dataframe from CSV

    """
    file = os.path.join(DATA_FOLDER,file)
    with open(file,"w") as tsvfile:
        df.to_csv(tsvfile,sep = sep)