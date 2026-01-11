from typing import List
import pandas as pd
from langchain_core.tools import tool
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_core.tools import create_retriever_tool
from langchain_openai import ChatOpenAI
from src.database import get_vector_store
Math_LLM = ChatOpenAI(model= "gpt-4o-mini", temperature=0)
@tool
def analyse_csv_file(file_paths: List[str], query : str) -> str:
    """
    Analyzes financial data from multiple CSV files. 
    Use this when you need to compare data across different years or reports.
    
    Args:
        file_paths (List[str]): A list of paths to the CSV files (e.g., ["data/2023.csv", "data/2024.csv"])
        query (str): The analysis question (e.g., "Calculate the year-over-year revenue growth")
    """
    dfs = []
    for path in file_paths:
        try:
            df = pd.read_csv(path)
            df['Source_File'] = path
            dfs.append(df)
        except Exception as e:
            return f"Error reading file {path}: {e}"
    if not dfs:
        return "No valid CSV files were provided"
    
    agent = create_pandas_dataframe_agent(
                Math_LLM,
                dfs,
                verbose = True,
                allow_dangerous_code= True,
                agent_type= "openai-tools")
    try:
        response = agent.invoke(query)
        return response['output']
    except Exception as e:
        return f"Error analysing csv: {str(e)}"
    
def get_tools():
    vector_store = get_vector_store()
    ret = vector_store.as_retriever(search_kwargs = {"k": 10})
    retrieval_tool = create_retriever_tool(
        ret,
        name="search_financial_reports",
        description = "Search for textual analysis, risk factors, and references (stubs) to tabular data in 10-K filings." 
    )
    return [retrieval_tool, analyse_csv_file]