from env import gdb
import os
import pandas as pd


def wrangle_zillow():
    '''
    The wrangle_zillow() function returns a DataFrame:
    --------------------------------------------------

    1. First the file is either unpickled locally,

        - or -

        a SQL query is run to pull the information from
        the codeup MySQL database. An env.py file is necessary.
        and the result is pickled for caching

    The DataFrame has df.shape: (2_985_217, 7)
    
    2. From there the approximately: 
        135_K rows with null or 0 data is dropped 

    The returned DataFrame has df.shape: (2_855_303, 7)

    '''
    # Set the filename to use for caching
    filename = 'zillow_data'

    # If the file is available locally, read it
    if os.path.isfile(filename):
        df = pd.read_pickle(filename)
        
    else:
        # Read the SQL query into a DataFrame
        df = gdb('zillow','''
        SELECT 	bedroomcnt beds, 
		bathroomcnt baths, 
		calculatedfinishedsquarefeet sqft, 
        taxvaluedollarcnt tax_appraisal, 
        yearbuilt yr_built,
        taxamount taxes,
        fips
        FROM properties_2017;
        ''')
    
    # Pickle the DataFrame for caching (pickling is much faster than using .csv)
    df.to_pickle(filename)

    # For now... we're just hacking and slashing with one command
    df = df.dropna()

    # NULL drop
    
    # There's still zeros in theh beds and baths columns, that's not right.
    no_beds_baths_index = df[(df.beds == 0) | (df.baths == 0)].index
    
    df = df.drop(index= no_beds_baths_index)

    return df

def get_zillow():
    '''
    This is basically the aqcuire function for the zillow data:
    -----------------------------------------------------------

    A DataFrame is returned with df. shape: (2_985_217, 7)

    The query used on the zillow schema on the codeup MySQL database:

    SELECT 	bedroomcnt AS beds, 
		bathroomcnt AS baths, 
		calculatedfinishedsquarefeet AS sqft, 
        taxvaluedollarcnt AS tax_appraisal, 
        yearbuilt AS yr_built,
        taxamount AS taxes,
        fips
        FROM properties_2017;
        
    If pickled and available locally as filename: 'zillow_data':

        The DataFrame is pulled from there instead.

    else:

        This will pickle the DataFrame and store it locally for next time
    '''
    # Set the filename for caching
    filename= 'zillow_data'
    
    # if the file is available locally, read it
    if os.path.isfile(filename):
        df = pd.read_pickle(filename)
        
    else:
        # Read the SQL query into a DataFrame
        df = gdb('zillow','''
        SELECT 	bedroomcnt beds, 
		bathroomcnt baths, 
		calculatedfinishedsquarefeet sqft, 
        taxvaluedollarcnt tax_appraisal, 
        yearbuilt yr_built,
        taxamount taxes,
        fips
        FROM properties_2017;
        ''')
    
    # Pickle the DataFrame for caching (pickling is much faster than using .csv)
    df.to_pickle(filename)
    return df