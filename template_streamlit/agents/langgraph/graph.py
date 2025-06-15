from typing import Annotated, Literal

from typing_extensions import TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode


class State(TypedDict):
    messages: Annotated[list, add_messages]


class BasicAgent:
    def __init__(self, llm, tools):
        self.tools = tools
        self.tool_node = ToolNode(
            tools=self.tools,
        )
        self.llm = llm
        # Bind the tools to the LLM
        self.llm = llm.bind_tools(self.tools)

    def call_model(self, state: State):
        messages = state["messages"]
        response = self.llm.invoke(messages)
        return {"messages": [response]}

    def should_continue(self, state: State) -> Literal["tools", END]:
        messages = state["messages"]
        last_message = messages[-1]
        # If the LLM makes a tool call, then we route to the "tools" node
        if last_message.tool_calls:
            return "tools"
        # Otherwise, we stop (reply to the user)
        return END

    def create_graph(self):
        graph_builder = StateGraph(State)

        # The first argument is the unique node name
        # The second argument is the function or object that will be called whenever
        # the node is used.
        graph_builder.add_node("agent", self.call_model)
        graph_builder.add_node("tools", self.tool_node)

        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edges(
            # First, we define the start node. We use `agent`.
            # This means these are the edges taken after the `agent` node is called.
            "agent",
            # Next, we pass in the function that will determine which node is called next.
            self.should_continue,
        )
        graph_builder.add_edge("tools", "agent")

        return graph_builder.compile()
