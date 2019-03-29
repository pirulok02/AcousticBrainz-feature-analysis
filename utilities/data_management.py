import pandas as pd 
from collections import defaultdict

def compute_instersection(*args):
    """Returns common elements in the iterables given

    Args:
        As many iterables as needed

    Return:
        intersection: elements common to all args

    """
    intersection = set(args[0])
    for arg in args[1:]:
        intersection = intersection & set(arg)
    return intersection

def get_most_frequent(df, N = 20):
    """Returns list of the generes more recurrent in df

    Args:
        df: dataframe

    Kwargs:
        N: number of generes to consider

    Return:
        intersection: elements common to all args

    """
    #declare counter default dictionary
    counter = defaultdict(int)

    #iterate through genre columns to create a subgenere counter
    for col in list(df)[1:]:
        
        #for each column, get the list of that column's values for all sound_ids
        col_values = df[col].tolist()
        
        #iterate in that list
        for genere in col_values:
            
            #if the genre has a subgenre, it will be of the format genre---subgenre, if it does not have a subgenre, ignore it
            try:
                subgenere = genere.split("---")[1]
            except(AttributeError,IndexError) as e:
                subgenere = ''
            if subgenere != '' : counter[genere] += 1

    #create dataframe for the default dictionary containing {Genere:Times it is mentioned}
    generespd = pd.DataFrame(list(counter.items()))

    #change dataframe's column and row values
    generespd.columns = ["Genere","Count"]
    generespd = generespd.set_index("Genere")

    #get only the N largest in the Count column
    generespd = generespd.nlargest(N, "Count")

    #convert the index to list in order to compare further on
    return generespd.index.tolist()

def reduce_df(df,to_keep):
    """Returns the elements of df that have at least one element of to_keep

    Args:
        df: dataframe
        to_keep: list of the generes to keep

    Return:
        df: dataframe with only the elements that have at least one element of to_keep

    """

    #iterate through the columns
    for col in df:
        
        #check for all the genres in most frequent and replace anything that is not there with a Nan
        df[col] = df[col].str.extract(r"\b^("+"|".join(to_keep)+r")\b")
        
    #Delete all rows and columns filled exclusively with Nan
    df = df.dropna(how='all').dropna(axis='columns',how='all')

    return df
    