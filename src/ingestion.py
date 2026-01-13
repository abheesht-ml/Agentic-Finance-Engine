import os
from dotenv import load_dotenv
load_dotenv()
from edgar import Company
from docling.document_converter import DocumentConverter
from src.input_schemas import InputfromUser, ProcessedDocument

def fetch_10k(data: InputfromUser) -> str:
    company = Company(data.company_ticker)
    input_val = data.years
    filing = None
    if input_val > 1900:
        filings = company.get_filings(form="10-K", year=input_val)
        if filings:
            filing = filings[0]
    else:
        filings = company.get_filings(form="10-K").latest(input_val)
        if input_val == 1:
            filing = filings
        elif filings:
            filing = filings[0]
    if not filing:
        raise ValueError(f"No 10-K found for {data.company_ticker}")
    save_dir = f"sec_filings/{data.company_ticker}/{filing.filing_date}"
    os.makedirs(save_dir, exist_ok=True)
    file_path = f"{save_dir}/full_report.html"
    if os.path.exists(file_path):
        return file_path
    try:
        html_content = filing.html()
        if html_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"Saved report to: {file_path}")
            return file_path
    except Exception as e:
        raise RuntimeError(f"Error saving file: {e}")
    raise FileNotFoundError("Could not download HTML.")

def html_to_hybrid(file_path: str, data: InputfromUser) -> ProcessedDocument:
    converter = DocumentConverter()
    result = converter.convert(file_path)
    doc = result.document 
    base_dir = os.path.dirname(file_path)
    csv_dir = os.path.join(base_dir, "extracted_tables")
    os.makedirs(csv_dir, exist_ok=True)
    table_summaries = []
    for i, table in enumerate(doc.tables):
        df = table.export_to_dataframe()
        csv_filename = f"table_{i}.csv"
        csv_full_path = os.path.join(csv_dir, csv_filename)
        df.to_csv(csv_full_path, index=False)
        
        summary = f"""
        \n[TABLE REFERENCE]
        Description: Data headers {list(df.columns)}
        Location: {csv_full_path}
        Action: Load this CSV with Pandas.
        \n"""
        table_summaries.append(summary)
    final_markdown_content = doc.export_to_markdown()
    final_markdown_content += "\n\n# DATA TABLES REFERENCE\n"
    for stub in table_summaries:
        final_markdown_content += stub
    return ProcessedDocument(
        content=final_markdown_content,
        metadata={
            "source": file_path, 
            "Company Ticker": data.company_ticker,
            "total_tables_extracted": len(table_summaries)
        }
    )