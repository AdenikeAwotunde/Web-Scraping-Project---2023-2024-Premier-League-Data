# Importing the necessary libraries
import pandas as pd
from bs4 import BeautifulSoup
import requests
import gspread
from google.oauth2.service_account import Credentials
import re

url =  "https://fbref.com/en/comps/9/2023-2024/2023-2024-Premier-League-Stats"
data= requests.get(url)
soup= BeautifulSoup(data.text, 'html.parser')
league_table= soup.select('table.stats_table')[0]

# Links to individual teams
links = league_table.find_all('a')
hrefs = [l.get('href') for l in links]
base_url = "https://fbref.com"
squad_links = [link['href'] for link in links if re.search(r'/en/squads/', link['href'])]

squad_urls = []  
for squad_link in squad_links:
    squad_urls.append(f"{base_url}{squad_link}")  # Append the generated URL to the list

# Main table
soup= BeautifulSoup(data.text, 'html.parser')
league_table= soup.select('table.stats_table')[0]

#
# Extract data, ensuring consistent row length
data = []
for row in league_table.find_all('tr'):
    cols = row.find_all('td')[:18]  # Truncate to 18 columns
    cols = [col.text.strip() for col in cols]
    data.append(cols)

#checking the number of columns in the table
num_columns = len(data[0])  # Assuming all rows have the same number of columns
print(num_columns) 


# Google Sheet setup function
def google_sheet_setup(service_account_path, sheet_name):
    creds = Credentials.from_service_account_file(
        service_account_path,
        scopes=[
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
    )
    client = gspread.authorize(creds)
    return client.open(sheet_name)

# Path to your service account JSON file
service_account_path = r"C:\Users\user\Desktop\Projects\Webscrapping Project\webscrapppingdb-40d589693f5b.json"
# Name of the Google Sheet
sheet_name = "2023-2024 EPL Database"

# Retrieve the Google Sheet
sheet = google_sheet_setup(service_account_path, sheet_name)

# Extracted headers from web scraping
headers = [th.text.strip() for th in league_table.find_all('th')]  # Example scraping logic
headers = headers[:18]  # Adjust the slicing as needed

#
# Add the "RK" column manually to the data
data_with_index = [[i] + row for i, row in enumerate(data)]

# Clear the sheet (optional to remove any previous data or blank row)
sheet.clear()

# Insert headers in the first row (index=1)
sheet.insert_row(headers, index=1)

# Insert data starting from the second row (index=2)
sheet.insert_rows(data_with_index, row=2)
sheet.delete_rows(2)

 #ing