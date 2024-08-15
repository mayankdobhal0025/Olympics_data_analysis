import pandas as pd


def preprocess(df,region_df):
    # filtering for Summer Olympics
    df = df[df['Season'] == "Summer"]
    #dropping Duplicates
    df.drop_duplicates(inplace = True)
    # one hot encoding and Concatenating to df
    df = pd.concat([df,pd.get_dummies(df["Medal"])],axis = 1)
    #merge with region_df
    df = df.merge(region_df, on = "NOC",how = "left")
    return df