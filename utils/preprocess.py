import pandas as pd
import numpy as np
import requests
from datetime import datetime


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

# def standardize_salary_test(base_currency, api_key, average_salary):
#     # Get exchange rate of base currency with all other ones.
#     exchange_rates = get_latest_exchange_rate(base_currency, api_key)

#     # 
#     standard_salary = {k: average_salary * v for k, v in exchange_rates.items()}

#     return pd.Series([base_currency, standard_salary])

# def standardize_salary(base_currency, api_key, df, average_salary_column='average_salary', currency_column='currency'):
#     """
#     Chuẩn hóa cột average_salary từ đơn vị tiền tệ hiện tại sang base_currency.
#     """
#     # Lấy tỷ giá hối đoái từ API
#     exchange_rates = get_latest_exchange_rate(base_currency, api_key)

#     # Hàm con chuẩn hóa từng hàng trong cột average_salary
#     def convert_salary(row):
#         current_currency = row[currency_column]
#         average_salary = row[average_salary_column]

#         # Kiểm tra nếu current_currency hợp lệ
#         if current_currency in exchange_rates and not pd.isna(average_salary):
#             rate = exchange_rates[current_currency]
#             standardized_salary = average_salary * rate
#             return standardized_salary
#         return np.nan  # Trả về NaN nếu có lỗi

#     # Áp dụng hàm convert_salary lên DataFrame
#     df['standardized_salary'] = df.apply(convert_salary, axis=1)
#     return df


def standardize_salary(base_currency, api_key, df, salary_column='average', currency_column='currency'):
    """
    Chuẩn hóa cột lương của DataFrame từ currency hiện tại sang base_currency.
    Trả về DataFrame với cột 'standardized_salary'.

    Args:
        base_currency (str): Tiền tệ chuẩn.
        api_key (str): API key để lấy tỷ giá.
        df (pd.DataFrame): DataFrame chứa cột lương và tiền tệ.
        salary_column (str): Tên cột chứa lương trung bình.
        currency_column (str): Tên cột chứa loại tiền tệ.

    Returns:
        pd.DataFrame: DataFrame với cột 'standardized_salary'.
    """
    # Lấy tỷ giá hối đoái
    exchange_rates = get_latest_exchange_rate(base_currency, api_key)

    # Chuyển đổi lương
    df['standardized_salary'] = df.apply(
        lambda row: row[salary_column] * exchange_rates.get(row[currency_column], np.nan)
        if pd.notna(row[salary_column]) and row[currency_column] in exchange_rates
        else np.nan,
        axis=1
    )
    return df
