import pandas as pd 
from collections import defaultdict
from IPython.display import clear_output

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

def organize_features_in_genre_dict(features_df, db_df, genres):
    """Reformats features_df in a dictionary of sub_generes

    Args:
        features_df: dataframe of rows:ids and cols:feaures
        db_df: dataframe of rows:ids and cols:generes
        genres: generes to consider

    Return:
        information: dictionary of subgenere : features

    """
    #initialize dictionary
    information = {}

    #loop through subgenres to create an entry in the dictionary for each subgenre where in each entry, a dictionary of
    #the features will be created in order to get a dictionary of features for each genre in an organised manner.
    for i,sub_genre in enumerate(genres):
        
        print("Processing {0} out of {1}".format(i+1,len(genres)))

        #temporal variable that copies the lastfm intersected N pandas matrix
        db_df_temp = db_df.copy()

        #iterate through columns for:
        #- All genres that are not the one in each iteration will be repaced with NaN
        #- All columns and sound ids that are not from that genere get deleted
        for col in db_df_temp:
            
            db_df_temp[col] = db_df_temp[col].str.extract(r"\b^("+sub_genre+r")\b")

        db_df_temp = db_df_temp.dropna(how='all').dropna(how='all',axis='columns')
        
        #initializing the features dictionary for each subgenre
        information[sub_genre] = {}
        
        #for each feature, add the list features for each subgenre to the dictionary
        for feature in list(features_df):
            
            #get only the feature that it's wanted
            temp = features_df[feature].to_frame()
            
            #get only the information for the genre for this iteration
            temp = temp.drop(set(temp.index.tolist())-set(db_df_temp.index.tolist()))
            
            #add entry to the dictionary
            information[sub_genre].update({ feature : temp[feature].tolist() })
        
        clear_output()

    print("Done!")

    return information

