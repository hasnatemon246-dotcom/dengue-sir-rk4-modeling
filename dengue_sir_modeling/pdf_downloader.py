import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib3

# Disable SSL warnings for the government website
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Target page URL
page_url = "https://old.dghs.gov.bd/index.php/bd/home/5200-daily-dengue-status-report"

# Request headers to simulate a web browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

# Directory to save the downloaded PDF files
download_dir = "dengue_press_releases"
os.makedirs(download_dir, exist_ok=True)

try:
    print("Fetching data from the website...")
    response = requests.get(page_url, headers=headers,
                            verify=False, timeout=20)
    response.encoding = 'utf-8'

    soup = BeautifulSoup(response.text, 'html.parser')

    target_pdf_urls = []

    # Extract all <a> tags from the page
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']

        # Filter URLs that contain 'dengue' and end with '.pdf'
        if 'dengue' in href.lower() and href.lower().endswith('.pdf'):
            full_url = urljoin("https://old.dghs.gov.bd/", href)

            # Avoid duplicate URLs
            if full_url not in target_pdf_urls:
                target_pdf_urls.append(full_url)

    print(
        f"Found a total of {len(target_pdf_urls)} Dengue Press Release PDFs.")

    # Select only the first 30 PDFs to download
    selected_pdfs = target_pdf_urls[:90]

    print("\nStarting download...\n" + "="*40)
    for index, pdf_url in enumerate(selected_pdfs, start=1):
        file_name = os.path.basename(pdf_url)
        file_path = os.path.join(download_dir, file_name)

        print(f"[{index}/90] Downloading: {file_name} ...")

        try:
            # Download the PDF file
            pdf_res = requests.get(
                pdf_url, headers=headers, verify=False, timeout=30)

            if pdf_res.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(pdf_res.content)
                print("   ✔ Successfully saved!")
            else:
                print(f"   ✖ Failed (Status Code: {pdf_res.status_code})")

        except Exception as err:
            print(f"   ✖ Download error: {err}")

    print("="*40)
    print(
        f"\nProcess completed! Successfully downloaded {len(selected_pdfs)} files into the '{download_dir}' folder.")

except Exception as e:
    print(f"Error accessing the website: {e}")
