from env import gdb
import os
import pandas as pd


def wrangle_zillow():
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

