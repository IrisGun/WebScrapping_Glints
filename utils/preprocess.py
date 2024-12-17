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

    if period == 'hour':
        lower *= 160  # Assuming 160 working hours in a month
        upper *= 160

    return pd.Series([period, currency, lower, upper, average])


def get_historical_exchange_rate(base_currency, date):
    """
    Lấy tỷ giá hối đoái từ một API hỗ trợ dữ liệu lịch sử.
    Trả về tỷ giá giữa base_currency và tất cả các loại tiền tệ khác vào ngày cụ thể.
    """
    formatted_date = f"{date[:4]}-{date[4:6]}-{date[6:]}"  # Định dạng YYYY-MM-DD
    api_url = f"https://api.exchangerate.host/{formatted_date}?base={base_currency}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            return data['rates']  # Trả về tất cả tỷ giá so với base_currency
        else:
            print(f"Không thể truy cập API tỷ giá: {response.status_code}")
            return {}
    except Exception as e:
        print(f"Lỗi khi lấy tỷ giá: {e}")
        return {}

def standardize_salary(average_salary, today, standard_currency):
    
    # Lấy tỷ giá lịch sử với tất cả các loại tiền tệ
    # Get exchange rate of base currency with all other ones.
    exchange_rates = get_historical_exchange_rate(standard_currency, today)

    # Chuyển đổi về các loại tiền tệ khác
    standard_salary = {k: average_salary * v for k, v in exchange_rates.items()}

    return pd.Series([standard_currency, standard_salary])
