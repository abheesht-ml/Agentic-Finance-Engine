import pandas as pd
from langchain_core.tools import tool
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import create_retriever_tool
from src.database import get_vector_store

Math_LLM = ChatOpenAI(model="gpt-4o-mini", temperature=0)
@tool
def analyze_csv_data(file_path: str, query: str) -> str:
    """
    Analyzes financial data from a CSV file using a pandas agent.
    
    Args:
        file_path: Absolute path to the CSV file.
        query: Analytical question to answer using the data.
    """
    try:
        df = pd.read_csv(file_path)
        agent = create_pandas_dataframe_agent(
            Math_LLM,
            df,
            verbose=True,
            allow_dangerous_code=True,
            agent_type="openai-functions"
        )
        response = agent.invoke(query)
        return response['output']
    except Exception as e:
        return f"Error analyzing CSV: {str(e)}"
def get_tools():
    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": 10})
    retriever_tool = create_retriever_tool(
        retriever,
        name="search_financial_reports",
        description="Search for text, risks and tables in the 10-K. Use this FIRST."
    )
    return [retriever_tool, analyze_csv_data]