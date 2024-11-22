import pandas as pd
def load_data():
    papers = pd.read_csv('data/Research_Papers_Table_with_All_Additional_Entries.csv')
    return papers