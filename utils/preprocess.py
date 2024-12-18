import pandas as pd
import numpy as np
import requests
from datetime import datetime
import json


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

    if period == 'hour':
        lower *= 160  # Assuming 160 working hours in a month
        upper *= 160

    return pd.Series([period, currency, lower, upper, average])


def get_historical_exchange_rate(base_currency, date, api_key):
    """
    Get exchange rate of a base currency to standardize the average salary to one unified unit
    from a specific date in the pass
    """
    formatted_date = f"{date[:4]}-{date[4:6]}-{date[6:]}"  # Định dạng YYYY-MM-DD
    api_url = f"https://api.exchangerate.host/{formatted_date}?base={base_currency}?access_key={api_key}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            return data['rates']  # Return all exchange rate compared to base_currency
        else:
            print(f"Can not access API: {response.status_code}")
            return {}
    except Exception as e:
        print(f"Error(s) occurred during API getting process {e}")
        return {}

def get_latest_exchange_rate(base_currency, api_key):
    """ Get exchange rate from the latest timestamp """
    api_url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            timestamp = datetime.now()
            try:
                with open(f"data\exchange_rate_{data['time_last_udpate_unix']}.json", "w") as file:
                    data.dump(data, file, indent=4)
            except Exception as e:
                print(f"Error(s) occurred during saving file")
            
            return data
        else:
            print(f"Can not access API: {response.status_code}")
    except Exception as e:
        print(f"Error(s) occurred during API getting process {e}")
        return None

def standardize_salary_from_api(base_currency, api_key, df, salary_column='average', currency_column='currency'):
    """
    Standardize salary column in df to a unified base_currency using API from exchange rate
    Return a DataFrame with column 'standardized_salary'.

    Args:
        base_currency (str): Currency used as standardized unit
        api_key (str): API key to get conversion rate from exchange rate API
        df (pd.DataFrame): df to preprocess
        salary_column (str): name of the column that contains salary data
        currency_column (str): name of the column that contains current currency data

    Returns:
        pd.DataFrame: DataFrame with column 'standardized_salary'.
    """
    # Lấy tỷ giá hối đoái
    exchange_rates = get_latest_exchange_rate(base_currency, api_key)

    # Chuyển đổi lương
    df['standardized_salary'] = df.apply(
        lambda row: round(row[salary_column] / exchange_rates.get(row[currency_column], np.nan))
        if pd.notna(row[salary_column]) and row[currency_column] in exchange_rates
        else np.nan,
        axis=1
    )

    return df

def standardize_salary_from_file(filename, df, base_currency="VND", salary_column='average', currency_column='currency'):
    """
    Standardize salary column in df to a unified base_currency using json file loaded in data folder
    Return a DataFrame with column 'standardized_salary'.
    """
    # Get conversion rate from file
    with open(f"data/{filename}", "r") as file:
        data = json.load(file)

    conversion_rates = data["conversion_rates"]

    # Standardize slary to base currrency
    df[f"standardize_salary_{base_currency}"] = df.apply(
        lambda row: round(row[salary_column] / conversion_rates.get(row[currency_column], np.nan)) 
        if pd.notna(row[salary_column]) and row[currency_column] in conversion_rates 
        else np.nan,
        axis=1
    )

    return df

def standardize_title(df, column="job_title"):
    """
    Capitalize the first letter of each word in the job_title column.
    """
    if column in df.columns:
        df[column] = df[column].str.title()
    return df


def filter_job_titles(df, keywords=['data', 'business intelligence']):
    """
    Filters the DataFrame to include only rows where the job_title contains specified keywords.
    """
    if "job_title" in df.columns:
        pattern = '|'.join(keywords)  # Create a regex pattern from the keywords
        filtered_df = df[df["job_title"].str.contains(pattern, case=False, na=False)]
        return filtered_df
    else:
        print("The 'job_title' column does not exist in the DataFrame.")
        return pd.DataFrame()  # Return an empty DataFrame if column is missing


