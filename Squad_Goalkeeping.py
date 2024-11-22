import requests
from bs4 import BeautifulSoup
import gspread
from google.oauth2.service_account import Credentials

# Define URL and Scrape
url = 'https://fbref.com/en/comps/9/2023-2024/keepersadv/2023-2024-Premier-League-Stats'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
advanced_goalkeeping = soup.select('table.stats_table')[0]

# Extacting Table headers
top_headers = [th.text.strip() for th in advanced_goalkeeping.find_all('tr')[0].find_all('th')]
sub_headers = [th.text.strip() for th in advanced_goalkeeping.find_all('tr')[1].find_all('th')]

# Preparing a two-row header for Google Sheets
top_headers[0] = "Squad"  
headers = [top_headers, sub_headers]

# Extracting data rows
data = []
for row in advanced_goalkeeping.find_all('tr')[2:]:  # Skip the first two rows (headers)
    first_col = row.find('th').text.strip() if row.find('th') else None
    cols = [col.text.strip() for col in row.find_all('td')]
    if first_col or cols:
        data.append([first_col] + cols)

# Google Sheets setup functiob
def google_sheet_setup(service_account_path, sheet_name):
    # Authenticate with Google Sheets
    creds = Credentials.from_service_account_file(
        service_account_path,
        scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    )
    client = gspread.authorize(creds)
    return client.open(sheet_name)

# Google Service Account JSON key
service_account_path = r"C:\Users\user\Desktop\Projects\Webscrapping Project\webscrapppingdb-40d589693f5b.json"  # Replace with your actual path
sheet_name = '2023-2024 EPL Database'  

# Initializing Google Sheets client
client = google_sheet_setup(service_account_path, sheet_name)

# Open the "Advanced Goalkeeping" sheet
try:
    worksheet = client.worksheet("Advanced Goalkeeping")  # Open the existing sheet
except gspread.exceptions.APIError:
    worksheet = client.add_worksheet(title="Advanced Goalkeeping", rows=100, cols=len(headers[1]))  # Create the sheet if it doesn't exist

# Adding Headers
existing_headers = worksheet.row_values(1)
if not existing_headers:  # If no headers exist in the first row
    worksheet.append_row([""] * len(headers[1]))  # Add a blank row at the top
    worksheet.append_row(headers[0])  # Add the first header row
    worksheet.append_row(headers[1])  # Add the second header row

# Add data rows to the sheet starting from the next available row
for row in data:
    worksheet.append_row(row)
