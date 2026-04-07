from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from tools import (
    calculate_budget,
    estimate_trip_cost,
    search_flights,
    search_hotels,
    suggest_itinerary,
)
from dotenv import load_dotenv

load_dotenv()

with open ("system_prompt.txt", "r", encoding ='utf-8') as f:
    SYSTEM_PROMT = f.read()

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

tools_list = [
    search_flights,
    search_hotels,
    calculate_budget,
    estimate_trip_cost,
    suggest_itinerary,
]
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools_list)

def agent_node(state: AgentState) -> str:
    messages = state["messages"]
    if not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMT)] + messages
    response = llm_with_tools.invoke(messages)  

    if response.tool_calls:
        for tc in response.tool_calls:
            print(f"Tool called: {tc['name']} with arguments {tc['args']}")
    else:
        print("Trả lơi trực tiếp")

    return {"messages": [response]}

builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)

tool_node = ToolNode(tools_list)
builder.add_node("tools", tool_node)

# khai báo edges 
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent",  tools_condition)
builder.add_edge("tools", "agent")

graph = builder.compile()

if __name__ == "__main__":
    print("TravelBuddy - Trợ lý du lịch Thông minh")

    while True:
        user_input = input("\nBạn: ").strip()
        if user_input.lower() in ["exit", "quit","q"]:
            break

        print("TravelBuddy đang suy nghĩ...")
        result = graph.invoke({"messages": [("human", user_input)]})
        final = result["messages"][-1]
        print("\nTravelBuddy: ", final.content)