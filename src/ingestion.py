import os
import pandas as pd
from edgar import Company
from docling.document_converter import DocumentConverter
from input_schemas import InputFromUser, ProcessedDocument

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
            os.makedirs(saved_path, exist_ok=True)
            save_path.append(saved_path)
        try:
            html_content = filing.html()
            with open(f"{saved_path}/full_report.html", "w", encoding="utf-8") as f:
                f.write(html_content)
        except Exception as e:
            print(f"Download failed: {e}")
    else:
        print(f"Fetching the last {years} reports")
        filings = company.get_filings(form= "10-K").latest(years)
        for reports in filings:
            current_path = f"sec_filings/{data.company_ticker_name}/{reports.filing_date}"
            os.makedirs(current_path, exist_ok=True)
            save_path.append(current_path)
            try:
                html_content = reports.html()
                with open(f"{current_path}/full_report.html", "w", encoding= "utf-8") as f:
                    f.write(html_content)
            except Exception as e:
                print(f"Download Failed for {reports.filing_date}: {e}")
    return save_path

def convert_to_hybrid(data: InputFromUser, save_path: str):
    converter = DocumentConverter()
    all_documents = []
    for folder_path in save_path:
        file_path = f"{folder_path}/full_report.html"
        result = converter.convert(file_path)
        base_dir = os.path.dirname(file_path)
        csv_dir = os.path.join(base_dir,"extracted tables")
        os.makedirs(csv_dir, exist_ok=True)
        table_summaries = []
        for i,table in enumerate (result.document.tables):
            df = table.export_to_dataframe()
            csv_filename = f"table_{i}.csv"
            csv_fullpath = os.path.join(csv_dir, csv_filename)
            df.to_csv(csv_fullpath, index = False)

            summary = f""" 
                    \n[TABLE REFERENCE]
                    Description: Data Headers {list(df.columns)}
                    Location: {csv_fullpath}
                    Action: Load this CSV with Pandas
                    \n"""
            table_summaries.append(summary)
        final_markdown_content = result.document.export_to_markdown()
        final_markdown_content += "\n\n# DATA TABLES REFERENCE"
        for stub in table_summaries:
            final_markdown_content += stub
        doc =  ProcessedDocument(
            content_document = final_markdown_content,
            metadata={
                "source" : file_path,
                "Company Ticker" : data.company_ticker_name,
                "total_tables_extracted" : len(table_summaries)
            }
        )
        all_documents.append(doc)
    return all_documents


        

        

        