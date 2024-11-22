# Web-Scraping-Project---2023/2024-Premier-League-Data  


## Project Overview
Web scraping extracts data from a website by sending HTTP requests and parsing the returned HTML.This project employs web scraping techniques to gather football data from the 2023/2024 Premier League season. The focus is to extract statistics such as final league table, top team scorers and advanced squad goalkeeping statistics; and then storing the extracted data into google sheets using google sheets API and Gspread library. The project aimed to achieve the following:
- Set up the web scraping environment by importing the necessary libraries.
- Set up the google sheet API integration for storing the data.
- Scrape the relevant data from the website by collecting information such as the final league table, top team scorers and advanced squad goalkeeping data.
- Clean the scraped data, perform calculations as needed and then store in google sheets using the GSpread library.

## Data Source
The data is from FBREF website, the 2023-2024 Premier League Season, See link below:
https://fbref.com/en/comps/9/2023-2024/2023-2024-Premier-League-Stats

## Tools and Libraries
- Python IDE(Visual Studio Code)
- Google Cloud Console (for google API integration)
- Google Sheet
- Python Libraries(Pandas, BeautifulSoup, Gspread, Requests, oauth2client)

## Methodology

### 1. Setting up the web scrapping environment 
This was done by unstallung the aforementioned libraries using pip
```python
pip install requests beautifulsoup4 pandas gspread oauth2client
```

### 2. Setting up Google Sheets API
To interact with Google Sheets, I needed to set up the Google Sheets API following these steps: 
- Create a Google Cloud project.
- Enable the Google Sheets API and Google Drive API.
- Create a service account and download the JSON credentials file.
- Share your Google Sheet with the service account email address to allow it to write data.

``` python
from google.oauth2.service_account import Credentials
import gspread

def google_sheet_setup(service_account_path, sheet_name):
    creds = Credentials.from_service_account_file(
        service_account_path,
        scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    )
    client = gspread.authorize(creds)
    return client.open(sheet_name)
```
  
### 3. Implementing web scraping
A scraper was built to extract re;evant data from the website while ensuring to check and respect the website policies with these steps:
- Sending a request to the target URL and parsing the HTML response using BeautifulSoup.
- Extracting relevant data, including headers and player/team statistics.
- Handling any issues with missing or incomplete data, ensuring the scraped data is reliable.
-  Data cleaning was done on the scraped data to remove irrelevant informationm calculated metrucs were also done as needed

```python
# Web scraping function
def scrape_premier_league_data():
    url = 'https://fbref.com/en/comps/9/2023-2024/keepersadv/2023-2024-Premier-League-Stats'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Scrape Squad Goalkeeping Table
    squad_goalkeeping = soup.select('table.stats_table')[0]
```

### 4. Google Sheets Integration
After cleaning the data, it was inserted into a Google Sheet for easy viewing and further analysis. The process involves:
- Connecting to Google Sheets: Using the gspread library to authenticate and interact with Google Sheets via the API.
- Creating or Selecting a Google Sheet: If the sheet doesn't exist, it will be created. If it already exists, the script will update the relevant sheet.
- Inserting Data: Append the cleaned data into the sheet, making sure not to overwrite any manually entered data or pre-existing content.
- Preserving Manual Changes: If the Google Sheet has manual edits that should be preserved, the script is designed to append new data starting from the second row or a new sheet section, avoiding overwriting existing information.

```python
existing_headers = worksheet.row_values(1)
    if not existing_headers:  # If no headers exist in the first row
        worksheet.append_row([""] * len(headers[1]))  # Add a blank row at the top
        worksheet.append_row(headers[0])  # Add the first header row
        worksheet.append_row(headers[1])  # Add the second header row

    # Add data rows to the sheet starting from the next available row
    for row in data:
        worksheet.append_row(row)
```

## Conclusion
The steps documented in this project allows for automatation of collecting data from websites while respecting the rules and policies of the site with respect to scraping data; and how to seamlessly integrate the extracted data into google sheets using google API.

## Recommendation
- Always check and respect the website’s robots.txt file and scraping policies.
- Ensure compliance with local and international web scraping laws, particularly regarding data usage.

## Limitation
- The scraping logic relies on the current HTML structure of the website. Any updates to the structure may break the scraper.
- For larger datasets or frequent updates, storing and processing data in Google Sheets may become slow and inefficient.

## References
https://realpython.com/python-web-scraping-practical-introduction/
https://gspread.readthedocs.io/en/latest/


