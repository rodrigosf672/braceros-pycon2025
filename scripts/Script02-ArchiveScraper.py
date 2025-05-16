import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# Base URL for Bracero Archive items
base_url = "https://braceroarchive.org/items/show/"

# Scrape a single page and return interview data
def scrape_interview(number):
    url = base_url + str(number)
    
    # Polite delay inside each thread
    time.sleep(random.uniform(0.5, 1.5))
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return None  # Skip failed requests

    soup = BeautifulSoup(response.content, "html.parser")
    
    # Extract the page title
    title = soup.find("h1").text.strip() if soup.find("h1") else "N/A"

    # Try to extract Q&A content using regex
    interview_text = ""
    for element in soup.find_all("div", class_="element-text"):
        text_content = element.get_text(separator=" ", strip=True)
        qa_content = re.findall(r"([A-Z]{2}:.*?)(?=[A-Z]{2}:|$)", text_content, re.DOTALL)
        if qa_content:
            interview_text = " ".join(qa_content)
            break

    # Skip entries with no actual Q&A content
    if not interview_text.strip():
        return None

    return {
        "Record Number": number,
        "Title": title,
        "Interview Text": interview_text,
        "URL": url
    }

# List of item IDs to scrape
page_numbers = list(range(1, 3309))  # Adjust as needed

# Store results
results = []

# Thread pool with up to 10 workers
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(scrape_interview, num): num for num in page_numbers}
    for future in tqdm(as_completed(futures), total=len(futures)):
        result = future.result()
        if result:
            results.append(result)

# Convert to DataFrame and save
df = pd.DataFrame(results)
df.to_csv("data/bracero_archive_interviews.csv", index=False)
print("Data saved to data/bracero_archive_interviews.csv")