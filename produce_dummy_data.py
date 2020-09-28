import pandas as pd
import numpy as np

def random_number(num, mean, sts=None):
    if not sts:
        sts = mean*.1
    np.random.seed(1)
    return np.random.normal(mean, sts, num).astype(int)

def produce_dummy_data(num=50):
    df = pd.DataFrame()
    df['price_annual'] = random_number(num, 450)
    df['time_to_dev_weeks'] = random_number(num, 52)
    print(df.head())

    df.to_csv('drug_data.csv')

produce_dummy_data()