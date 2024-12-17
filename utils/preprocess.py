import pandas as pd
import numpy as np



def process_salary(salary):
    if pd.isna(salary):
        return pd.Series([np.nan, np.nan, np.nan, np.nan, np.nan])
    
    # Extract payment period
    period = salary.split('/')[-1]
    
    # Extract currency
    currency = ''.join([char for char in salary if char.isalpha() and char.isupper()])
    
    # Extract lower and upper bounds
    numbers = salary.replace(currency, '').replace(period, '').replace('.', '').replace(',', '').strip()
    numbers = numbers.rstrip('/')  # Remove trailing '/'
    
    if '-' in numbers:
        lower, upper = numbers.split('-')
        lower, upper = int(lower.strip()), int(upper.strip())
    else:
        lower = int(numbers.strip())
        upper = lower

    # Calculate average
    average = (lower + upper) / 2

    return pd.Series([period, currency, lower, upper, average])

def process_salary(salary):
    if pd.isna(salary):
        return pd.Series([np.nan, np.nan, np.nan, np.nan, np.nan])
    
    # Extract payment period
    period = salary.split('/')[-1]
    
    # Extract currency
    currency = ''.join([char for char in salary if char.isalpha() and char.isupper()])
    
    # Extract lower and upper bounds
    numbers = salary.replace(currency, '').replace(period, '').replace('.', '').replace(',', '').strip()
    numbers = numbers.rstrip('/')  # Remove trailing '/'
    
    if '-' in numbers:
        lower, upper = numbers.split('-')
        lower, upper = int(lower.strip()), int(upper.strip())
    else:
        lower = int(numbers.strip())
        upper = lower

    # Calculate average
    average = (lower + upper) / 2

    return pd.Series([period, currency, lower, upper, average])
