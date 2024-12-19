import os
import json
import requests
from bs4 import BeautifulSoup
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

# Load Credentials from JSON and Write to .env
class EnvFileCreator:
    def __init__(self, json_path, env_path=".env"):
        self.json_path = json_path
        self.env_path = env_path

    def create_env_file(self):
        """Read credentials from JSON and write to .env file."""
        with open(self.json_path, 'r') as file:
            creds = json.load(file)

        # Write to .env file
        with open(self.env_path, 'w') as env_file:
            env_file.write(f"PRIVATE_KEY={json.dumps(creds['private_key'])}\n")
            env_file.write(f"CLIENT_EMAIL={creds['client_email']}\n")
            env_file.write(f"PROJECT_ID={creds['project_id']}\n")
            env_file.write(f"TOKEN_URI={creds['token_uri']}\n")

        print(".env file created successfully!")

#Google Sheets Authentication
class GoogleSheetsAuth:
    def authenticate(self, scopes):
        """Authenticate using environment variables."""
        load_dotenv()  
        credentials_dict = {
            "type": "service_account",
            "project_id": os.getenv("PROJECT_ID"),
            "private_key": os.getenv("PRIVATE_KEY").replace('\\n', '\n'),  # format Json
            "client_email": os.getenv("CLIENT_EMAIL"),
            "token_uri": os.getenv("TOKEN_URI"),
        }
        creds = Credentials.from_service_account_info(credentials_dict, scopes=scopes)
        return gspread.authorize(creds)

#  Web Scraper Class
class EPLDataScraper:
    def __init__(self, url):
        self.url = url

    def scrape_data(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        advanced_goalkeeping = soup.select('table.stats_table')[0]

        # Extract headers
        top_headers = [th.text.strip() for th in advanced_goalkeeping.find_all('tr')[0].find_all('th')]
        sub_headers = [th.text.strip() for th in advanced_goalkeeping.find_all('tr')[1].find_all('th')]
        top_headers[0] = "Squad"
        headers = [top_headers, sub_headers]

        # Extract data rows
        data = []
        for row in advanced_goalkeeping.find_all('tr')[2:]:
            first_col = row.find('th').text.strip() if row.find('th') else None
            cols = [col.text.strip() for col in row.find_all('td')]
            if first_col or cols:
                data.append([first_col] + cols)
        return headers, data

# Google Sheets Handler
class GoogleSheetHandler:
    def __init__(self, client, sheet_name, sheet_title):
        self.client = client
        self.sheet_name = "2023-2024 EPL Database"
        self.sheet_title = "Goalkeeping"

    def write_data(self, headers, data):
        sheet = self.client.open(self.sheet_name)
        try:
            worksheet = sheet.worksheet(self.sheet_title)
        except gspread.exceptions.WorksheetNotFound:
            worksheet = sheet.add_worksheet(self.sheet_title, rows=100, cols=len(headers[1]))

        # Add headers
        if not worksheet.row_values(1):
            worksheet.append_row([""] * len(headers[1]))  # Blank row
            worksheet.append_row(headers[0])
            worksheet.append_row(headers[1])

        # Add data rows
        for row in data:
            worksheet.append_row(row)

#  Main Workflow
def main():
    # Paths and URLs
    json_path = "C:/Users/user/Desktop/Projects/Webscrapping Project/credentialls.json"
    env_path = "C:/Users/user/Desktop/Projects/Webscrapping Project/.env"
    url = "https://fbref.com/en/comps/9/2023-2024/keepersadv/2023-2024-Premier-League-Stats"
    sheet_name = "2023-2024 EPL Database"
    sheet_title = "Goalkeeping"

    #  Create .env file from JSON
    env_creator = EnvFileCreator(json_path, env_path)
    env_creator.create_env_file()

    #  Authenticate Google Sheets
    auth = GoogleSheetsAuth()
    client = auth.authenticate(scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"])

    # Scrape data
    scraper = EPLDataScraper(url)
    headers, data = scraper.scrape_data()

    # Write to Google Sheets
    sheet_handler = GoogleSheetHandler(client, sheet_name, sheet_title)
    sheet_handler.write_data(headers, data)

    print("Data successfully written to Google Sheets.")

if __name__ == "__main__":
    main()
