import pandas as pd
import numpy as np
import random
import string

random.seed(1)
np.random.seed(1)

def random_number(num, mean, sts=None):
    if not sts:
        sts = mean*.1
    return np.random.normal(mean, sts, num).astype(int)

def random_string(choices=string.ascii_lowercase, k=13):
    return ''.join(random.choices(string.ascii_lowercase, k=k))

def produce_dummy_data(num=50):
    df = pd.DataFrame()
    df['price_annual'] = random_number(num, 450)
    df['time_to_dev_weeks'] = random_number(num, 52)


    df['name'] = df.price_annual.apply(random_string)
    df.set_index('name', inplace=True)
    print(df.head())

    df.to_csv('drug_data.csv')

produce_dummy_data()