"""
Agent graph definition using LangGraph.
"""

from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.nodes import AgentNodes

def create_workflow():
    """Create and compile the LangGraph workflow"""
    
    # Initialize nodes
    nodes = AgentNodes()
    
    # Create graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("parse_logs", nodes.parse_logs_node)
    workflow.add_node("enrich_data", nodes.enrich_data_node)
    workflow.add_node("generate_solutions", nodes.generate_solutions_node)
    workflow.add_node("build_report", nodes.build_report_node)
    
    # Define edges (Parallel flow via enrich_data)
    workflow.set_entry_point("parse_logs")
    workflow.add_edge("parse_logs", "enrich_data")
    workflow.add_edge("enrich_data", "generate_solutions")
    workflow.add_edge("generate_solutions", "build_report")
    workflow.add_edge("build_report", END)
    
    # Compile
    app = workflow.compile()
    
    return app
