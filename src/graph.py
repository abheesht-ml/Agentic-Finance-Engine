import operator
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from src.tools import get_tools
from typing import Annotated, List, TypedDict

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
def agent_node(state: AgentState):
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    tools = get_tools()
    llm_with_tools = llm.bind_tools(tools)
    sys_msg = SystemMessage(content="""
    You are a Financial Analyst. 
    1. First, search the reports using 'search_financial_reports'.
    2. If you see a file path for a table, YOU MUST use the tool 'analyze_csv_data'.
    3. Synthesize the final answer.
    """)
    messages = [sys_msg] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def build_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", agent_node)
    tools = get_tools()
    tool_node = ToolNode(tools)
    workflow.add_node("tools", tool_node)
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent", tools_condition)
    workflow.add_edge("tools", "agent")
    app = workflow.compile() 
    return app