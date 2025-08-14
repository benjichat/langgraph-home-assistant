# main.py
from langgraph.graph import MessagesState, StateGraph, START, END
from agents.supervisor import supervisor_node
from utils.react_agent_factory import create_agent_node
from rich.pretty import Pretty
from rich import print as rprint

# Import the shared members list
from agents_config import members

class State(MessagesState):
    ext: str

builder = StateGraph(State)
builder.add_edge(START, "supervisor")
builder.add_node("supervisor", supervisor_node)

# Loop through the members list to add each agent node
for member in members:
    builder.add_node(member, create_agent_node(member))
graph = builder.compile()
graph.name = "Home Assistant"

### Visualize the agent graph using Mermaid syntax ###
mermaid_diagram = graph.get_graph().draw_mermaid()
rprint("[bold cyan]Agent Graph Visualization (Mermaid):[/bold cyan]")
rprint(mermaid_diagram)
rprint("------- PASTE INTO https://mermaid.live/ -------")


### For running via terminal, comment out if running via LangGraph Studio or API ###
input_data = {
    "messages": [("user", "fetch all events from the personal calendar tomorrow")]
 }
 
for s in graph.stream(input_data, subgraphs=True):
    rprint(Pretty(s))
    rprint("-" * 50)