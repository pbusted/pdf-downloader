# PDF Downloader

This project is a Python script designed to download PDF files from URLs listed in an Excel spreadsheet. The script uses multithreading to download multiple files simultaneously and logs the download process.


## Features

- Reads URLs from an Excel file.

- Downloads PDF files from the URLs.

- Supports multithreading for faster downloads.

- Logs download activities and errors.


## Requirements

- Python 3.x

- pandas

- requests

- validators

- concurrent.futures (for multithreading)


## Installation

1. Clone the repository:

```bash
git clone https://github.com/pbusted/pdf-downloader.git

cd pdf-downloader
```

3. Create a virtual environment:

```bash
python3 -m venv .venv
```

4. Activate the virtual environment:

```bash
source .venv/bin/activate
```

5. Install the required Python packages, using the provided `requirements.txt` file:

```bash
python3 -m pip install -r requirements.txt
```


## Usage

1. Place your Excel file with URLs in the project directory. The Excel file should have columns named `Pdf_URL`, `Report Html Address`, and `BRnum`.

2. Update the `input_file` variable in `pdf_download.py` with the path to your Excel file:

```python
input_file = 'your_excel_file.xlsx'
```

3. Run the script:

```bash
python pdf_download.py
```

4. The downloaded PDFs will be saved in the `downloaded_pdfs` directory.


## Logging

The script logs its activities to a file named `download_log.log`. This includes information about successful downloads and any errors encountered.