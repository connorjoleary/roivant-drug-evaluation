import pandas as pd
import numpy as np
import random
import string

random.seed(1)
np.random.seed(1)

def random_number(num, mean, sts=None, integer=True):
    if not sts:
        sts = mean*.1
    if integer:
        return abs(np.random.normal(mean, sts, num).astype(int))
    return abs(np.random.normal(mean, sts, num))

def random_string(blank='', choices=string.ascii_lowercase, k=13, return_type='string'):
    if k=='any':
        k=random.random()*len(choices)

    if return_type=='list':
        return random.sample(choices, int(k))

    elif return_type=='bool':
        return bool(random.getrandbits(1))
    return ''.join(random.choices(choices, k=int(k)))

def produce_dummy_data(num=25):
    df = pd.DataFrame()
    df['price_annual'] = random_number(num, 450000)
    df['time_to_dev_weeks'] = random_number(num, 52, 52)
    df['cost_to_create_annual'] = random_number(num, 250000)
    df['price_over_time'] = df.price_annual.apply(random_string, choices=['increasing', 'decreasing'], k=1, return_type='list')

    df['patents_affected_by_drug_percent'] = random_number(num, 60, sts=20)
    df['patents_developed_inhibitors_percent'] = random_number(num, 60, sts=20)
    df['patents_died_during_trials_percent'] = random_number(num, 2, sts=3, integer=False)
    df['side_effects'] = df.price_annual.apply(random_string, choices=['Nausea', 'Weakness', 'Headache', 'Confusion', 'Coughing up blood'], k='any', return_type='list')
    df['works_with_inhibitors'] = df.price_annual.apply(random_string, return_type='bool')


    # price over time
    # Sentiment of reviews
    # Number of people taking it over time


    df['name'] = df.price_annual.apply(random_string)
    df.set_index('name', inplace=True)
    print(df.head())

    df.to_csv('drug_data.csv')

produce_dummy_data()