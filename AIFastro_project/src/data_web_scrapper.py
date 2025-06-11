"""
This script performs a search and extracts information from scientific papers in the IAF (International Astronautical Federation) database.

The script follows these steps:
1. **Define Helper Functions**:
   - `is_valid_url(url)`: Checks if a URL is valid.
   - `get_additional_info(url)`: Extracts additional information (Paper ID and abstract) from a valid URL.

2. **Configure Search Parameters**:
   - `searches_list`: List of search terms to query the IAF database.
   - `results_pages_list`: List of page parameters to access different ranges of results.

3. **Search and Data Extraction**:
   - Iterates over each search term and each results page.
   - Sends an HTTP request to retrieve the HTML content of the search results page.
   - Extracts data from a results table, including authors, title, publication, year, and article link.
   - Corrects malformed URLs and extracts additional information (Paper ID and abstract) from each link.
   - Accumulates results in a DataFrame and saves it as a CSV file.

Requirements:
- `pandas`: For handling and saving data in CSV format.
- `requests`: For making HTTP requests.
- `BeautifulSoup` (from `bs4`): For parsing HTML content.
- `urllib.parse`: For validating URLs.

Note: The script assumes that the HTML structure of the results pages and articles is consistent with the expected structure in the code.
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def is_valid_url(url):
    """
    Checks if a URL is valid.

    Parameters:
    url (str): The URL to check.

    Returns:
    bool: True if the URL is valid (has scheme and domain), False otherwise.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def get_additional_info(url):
    """
    Extracts additional information (Paper ID and abstract) from a valid URL.

    Parameters:
    url (str): The article's URL.

    Returns:
    tuple: (paper_id, abstract), where:
        - paper_id (str): The extracted paper ID from the page, or None if not found.
        - abstract (str): The extracted abstract from the page, or None if not found.
    """
    if not is_valid_url(url):
        print(f"Invalid URL: {url}")
        return None, None
    try:
        print(f"Fetching URL: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(response.content, 'html.parser')

        paper_id_tag = soup.find('dt', id='item.papernumber')
        paper_id = paper_id_tag.find_next_sibling('dd').text.strip() if paper_id_tag else None

        abstract_tag = soup.find('dt', id='item.abstract')
        abstract = abstract_tag.find_next_sibling('dd').text.strip() if abstract_tag else None

        return paper_id, abstract
    except requests.exceptions.Timeout:
        print(f"Timeout error fetching URL: {url}")
        return None, None
    except requests.exceptions.ConnectionError:
        print(f"Connection error fetching URL: {url}")
        return None, None
    except (requests.RequestException, AttributeError) as e:
        print(f"Error fetching URL: {url}, Error: {e}")
        return None, None

# List of search terms
searches_list = [
    'industrial+design'
    , 'Strategic+Design'
    , 'UX'
    , 'UI'
    , 'Communication+Design'
    , 'Service+Design'
    , 'Fashion+Design'
    , 'User+Research'
    , 'Future+Foresight'
    , 'Interior+Design'
    , 'Engineering+Design'
]

# List of page parameters to access different result ranges
results_pages_list = [
    '&o=0&l=10&l=500',  # 0-500
    '&o=0&l=500&o=500',  # 501-1000
    # ... (other ranges omitted for brevity) ...
    '&o=16500&l=500&o=17000'   # 17001-17500
]

# Iterate over the list of search terms
for search in searches_list:
    # Create an empty DataFrame to accumulate all results
    df_total = pd.DataFrame(columns=['Authors', 'Title', 'Publication', 'Year', 'Link', 'Paper ID', 'Abstract'])

    for page in results_pages_list:
        search_url = 'https://dl.iafastro.directory/search/?q=' + search + page
        print("Search URL: ", search_url)

        # Perform the search on the page
        response = requests.get(search_url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the results table
        table = soup.find('table', class_='resultset')
        if not table:
            print(f"No table found for {search} on page {page}")
            continue

        # Extract information from the table
        rows = table.find_all('tr')[1:]  # Skip the table header
        data = []

        for row in rows:
            cols = row.find_all('td')
            authors = [author.text for author in cols[0].find_all('li')]
            title = cols[1].find('a').text
            link = 'https://dl.iafastro.directory' + cols[1].find('a')['href']
            publication = cols[2].text.strip()
            year = cols[3].text.strip()
            data.append([authors, title, publication, year, link])

        # Create a temporary DataFrame with the results from this page
        df = pd.DataFrame(data, columns=['Authors', 'Title', 'Publication', 'Year', 'Link'])

        # If the DataFrame is empty, skip to the next iteration
        if df.empty:
            print(f"No data found for {search} on page {page}")
            continue

        # Correct malformed URLs
        df['Link'] = df['Link'].str.replace('..', '.')

        # Add additional information to the DataFrame
        additional_data = df['Link'].apply(get_additional_info)
        df['Paper ID'] = additional_data.apply(lambda x: x[0] if x else None)
        df['Abstract'] = additional_data.apply(lambda x: x[1] if x else None)

        # Accumulate results in df_total
        df_total = pd.concat([df_total, df], ignore_index=True)

    # Save the accumulated DataFrame after processing all pages
    df_total.to_csv(f'IAF_Papers_with_abstracts_{search}.csv', index=False)
    print(f'IAF_Papers_with_abstracts_{search}.csv successfully saved.')
