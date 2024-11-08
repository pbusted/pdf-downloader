import pandas as pd
import requests
import os
from concurrent.futures import ThreadPoolExecutor
import validators
import logging

# Configure logging
logging.basicConfig(filename='download_log.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Create a directory to store the downloaded PDFs, if it doesn't exist
output_dir = 'downloaded_pdfs'
os.makedirs(output_dir, exist_ok=True)

# Function to read the Excel file and filter rows with empty URLs
def load_data(file_path):
    df = pd.read_excel(file_path)
    return df # Return the DataFrame as is

# Function to download a single PDF file
def download_file(url, output_dir, file_name):
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Write PDF content in chunks to avoid loading large files into memory
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        logging.info(f"Downloaded: {file_name}")
        return True
    except requests.exceptions.RequestException as e:
        error_message = str(e).split(' for url: ')[0]
        logging.error(f"Error downloading {file_name}: {error_message}")
        return False

# Function to download PDFs with max 5 simultaneous downloads
def download_reports(df, output_dir, volume=50):
    with ThreadPoolExecutor(max_workers=5) as executor:
        for index, row in df.head(volume).iterrows(): # Limit DataFrame to first x (volume) lines for testing purposes
            if not pd.isnull(row['Pdf_URL']) and validators.url(row['Pdf_URL']):
                executor.submit(download_file, row['Pdf_URL'], output_dir, row['BRnum'] + '.pdf')
            elif not pd.isnull(row['Report Html Address']) and validators.url(row['Report Html Address']):
                executor.submit(download_file, row['Report Html Address'], output_dir, row['BRnum'] + '.pdf')
            else:
                logging.warning(f"Skipping {row['BRnum']}: No valid URL found")

if __name__ == '__main__':
    # Indicate the start of the download process
    print("Starting PDF download...")

    input_file = 'GRI_2017_2020.xlsx' # Path to spreadsheet with URLs

    # Load the data from the spreadsheet
    df = load_data(input_file)

    # Start downloading the PDFs
    download_reports(df, output_dir)
    print("All downloads completed!")