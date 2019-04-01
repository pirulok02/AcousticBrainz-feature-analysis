import os
import matplotlib.pyplot as plt
from utilities.constants import *
from IPython.display import clear_output
from collections import defaultdict
import numpy as np

def plotbar(feature_name,counter,percentage,directory):
    """Plots non numerical features as a barplot

    Args:
        feature_name: feature to be plotted
        counter: dictionary of occurrrences for the feature
        percentage: bool if the feature is wanted in percentage or in raw values
        directory: string with the path where to save the output plot
    """
    file = os.path.join(directory,"{}.{}".format(feature_name,'png'))
    
    #initialize plot and axes objects
    fig, ax = plt.subplots()
    opacity = 0.8
    
    #get the strings for the features that will be on the legend.
    indexes_str = list(counter[list(counter.keys())[0]].keys())
    
    #get the genre strings and ints(for multibar plot purposes)
    genre_index_int = np.arange(len(list(counter.keys())))
    genre_index_str = list(counter.keys())
    
    #set the value of the bar width according to the number of bar that have to be plotted in each x value
    bar_width = 1/(1.25*len(indexes_str))
    
    #for multibar plot purposes
    i = 0
    
    #calculate the sum of values for each subgenre in order to normalize if desired
    norm_array = [] 
    for sub_genre in genre_index_str:
        norm = 0
        for index in indexes_str:
            norm += counter[sub_genre][index]
        norm_array.append(norm)
    
    #for each value of the legend:
    for index in indexes_str:
        
        #list of values to print
        val = []
        
        #for each value in x axis
        for sub_genre in counter.keys():
            
            #add the corresponding value to the list
            val.append(counter[sub_genre][index])
            
        if percentage:
            val[:] = [100*x/norm for x,norm in zip(val,norm_array)]
        
        #print the rectangle
        rects1 = plt.bar(genre_index_int + i*bar_width, val, bar_width, alpha=opacity, label=index)
        
        #for multibar plot purposes
        i += 1
        

    plt.xlabel('Genre')
    if percentage:
        plt.ylabel('Percentage')
    else:
        plt.ylabel('Appearances')
    plt.title(feature_name)
    plt.xticks(genre_index_int + i/2*bar_width, genre_index_str )
    plt.setp(ax.xaxis.get_majorticklabels(),rotation=45,ha="right")
    plt.legend()
    fig.set_size_inches(15,10)
    plt.savefig(file, dpi=100)
    plt.close()

def plotbox(feature_name,list_data,list_names,directory):
    """Plots numerical features as boxplots

    Args:
        feature_name: feature to be plotted
        list_data: data of the feature for the generes
        list_names: list of the names of the generes
        directory: string with the path where to save the output plot
    """
    file = os.path.join(directory,"{}.{}".format(feature_name,'png'))
    
    #initalize figure and axis
    fig, ax = plt.subplots()
    
    #set title
    ax.set_title(feature_name)
    
    #plot the data with the list given horizontally
    ax.boxplot(list_data,labels=list_names,vert=False)
    
    fig.set_size_inches(15,10)
    plt.savefig(file, dpi=100)
    plt.close()

def plot_all_features(information, features_df, genres):
    #loop though the features
    for i,feature in enumerate(list(features_df)):
    
        print("Processing {0} out of {1}".format(i+1,len(genres)))
        
        #if the feature selected is the tonal key or the tonal scale:
        #- loop for each subgenre
        #- count the times a feature is repeated for each genre
        #- call plotbar function
        if (feature == 'tonal.key_key') | (feature == 'tonal.key_scale'):
            counter = {}
            for sub_genre in genres:
                counter[sub_genre] = defaultdict(int)
                str_list = information[sub_genre][feature]
                for item in str_list:
                    counter[sub_genre][item] += 1
            plotbar( feature_name = feature, counter = counter,
                    percentage = True, directory = IMAGE_FOLDER)
        
        #if the feature is any other:
        #- get the data and store it in a list of arrays of data synced with the genres features labels
        #- call plotbox function
        else:
            list_data = []
            list_names = genres
            for sub_genre in genres:
                list_data.append(information[sub_genre][feature])
            
            plotbox( feature_name=feature, list_data=list_data, 
                    list_names=list_names, directory = IMAGE_FOLDER)
            
        clear_output()

    print("Done!")