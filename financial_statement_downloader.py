import os
import requests
import pandas as pd
from dotenv import load_dotenv

def download_financial_statement(ticker, statement, api_key):
    # Define the URL with the API key
    url = f'https://www.alphavantage.co/query?function={statement}&symbol={ticker}&apikey={api_key}'

    # Make the HTTP request through the SEC and load data into a DataFrame
    response = requests.get(url)
    data = response.json()
    if 'annualReports' in data:
        if isinstance(data['annualReports'], list):
            df = pd.DataFrame(data['annualReports'])
        else:
            df = pd.DataFrame([data['annualReports']], index=[0])
    else:
        df = pd.DataFrame([data], index=[0])  # Assumes data is a dictionary of scalars

    # Sort the DataFrame by 'Fiscal Date Ending' if applicable
    if 'fiscalDateEnding' in df.columns:
        df.sort_values(by='fiscalDateEnding', ascending=False, inplace=True)

    # Define directory and file path for the CSV
    directory_path = './financial_statements'
    os.makedirs(directory_path, exist_ok=True)  # Ensure the directory exists
    csv_filepath = os.path.join(directory_path, f'{ticker}_{statement.lower()}.csv')

    # Save the DataFrame to CSV
    df.to_csv(csv_filepath, index=False)

    # Verify the statement was attained for further AI Agent work
    print(f"CSV file saved successfully at {csv_filepath}")
    return csv_filepath
