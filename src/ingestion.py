import os
import pandas as pd
from edgar import Company
from docling.document_converter import DocumentConverter
from input_schemas import InputFromUser

def fetch_10k_filing(data: InputFromUser):
    company = Company(data.company_ticker_name)
    years = data.years_of_files
    filing = None
    save_path = []
    if years > 1900:
        print(f"Fetching the file of year: {years}")
        filings = company.get_filings(form = "10-K", year=years)
        if filings:
            filing = filings[0]
            saved_path = f"sec_filings/{data.company_ticker_name}/{filing.filing_date}"
            os.makedirs(save_path, exist_ok=True)
            save_path.append(saved_path)
    else:
        print(f"Fetching the last {years} reports")
        filings = company.get_filings(form= "10-K").latest(years)
        for reports in filings:
            save_path.append(f"sec_filings/{data.company_ticker_name}/{reports.filing_date}")
        for paths in save_path:
            os.makedirs(paths, exist_ok=True)
    return save_path


        

        

        