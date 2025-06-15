from logging import getLogger
from os import getenv

import streamlit as st
from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent, load_tools
from langchain_core.messages import AIMessage, HumanMessage
from langchain_ollama import ChatOllama
from langchain_openai import AzureChatOpenAI

from streamlit_utils import get_streamlit_cb, invoke_graph
from template_streamlit.agents.langgraph.graph import BasicAgent
from template_streamlit.agents.langgraph.tools import get_tools

load_dotenv(override=True)
logger = getLogger(__name__)

with st.sidebar:
    "# Agent"
    agent = st.selectbox(
        label="Active Agent",
        options=[
            "react",
            "basic_langgraph",
        ],
        index=0,
        key="agent",
    )
    "# Model"
    model_choice = st.radio(
        label="Active Model",
        options=["azure", "ollama"],
        index=0,
        key="model_choice",
    )
    "# Settings"
    if model_choice == "azure":
        azure_openai_endpoint = st.text_input(
            label="AZURE_OPENAI_ENDPOINT",
            value=getenv("AZURE_OPENAI_ENDPOINT"),
            key="AZURE_OPENAI_ENDPOINT",
            type="default",
        )
        azure_openai_api_key = st.text_input(
            label="AZURE_OPENAI_API_KEY",
            value=getenv("AZURE_OPENAI_API_KEY"),
            key="AZURE_OPENAI_API_KEY",
            type="password",
        )
        azure_openai_api_version = st.text_input(
            label="AZURE_OPENAI_API_VERSION",
            value=getenv("AZURE_OPENAI_API_VERSION"),
            key="AZURE_OPENAI_API_VERSION",
            type="default",
        )
        azure_openai_gpt_model = st.text_input(
            label="AZURE_OPENAI_GPT_MODEL",
            value=getenv("AZURE_OPENAI_GPT_MODEL"),
            key="AZURE_OPENAI_GPT_MODEL",
            type="default",
        )
        "[Azure Portal](https://portal.azure.com/)"
        "[Azure OpenAI Studio](https://oai.azure.com/resource/overview)"
        "[View the source code](https://github.com/ks6088ts-labs/template-streamlit)"
    else:
        ollama_model = st.text_input(
            label="OLLAMA_MODEL",
            value=getenv("OLLAMA_MODEL"),
            key="OLLAMA_MODEL",
            type="default",
        )
        "[Ollama Docs](https://github.com/ollama/ollama)"
        "[View the source code](https://github.com/ks6088ts-labs/template-streamlit)"


def is_azure_configured():
    return (
        st.session_state.get("AZURE_OPENAI_API_KEY")
        and st.session_state.get("AZURE_OPENAI_ENDPOINT")
        and st.session_state.get("AZURE_OPENAI_API_VERSION")
        and st.session_state.get("AZURE_OPENAI_GPT_MODEL")
        and st.session_state.get("model_choice") == "azure"
    )


def is_ollama_configured():
    return st.session_state.get("OLLAMA_MODEL") and st.session_state.get("model_choice") == "ollama"


def is_configured():
    return is_azure_configured() or is_ollama_configured()


def get_model():
    if is_azure_configured():
        return AzureChatOpenAI(
            azure_endpoint=st.session_state.get("AZURE_OPENAI_ENDPOINT"),
            api_key=st.session_state.get("AZURE_OPENAI_API_KEY"),
            openai_api_version=st.session_state.get("AZURE_OPENAI_API_VERSION"),
            azure_deployment=st.session_state.get("AZURE_OPENAI_GPT_MODEL"),
            temperature=0.0,
            streaming=True,
        )
    elif is_ollama_configured():
        return ChatOllama(
            model=st.session_state.get("OLLAMA_MODEL", ""),
            temperature=0.0,
            streaming=True,
        )
    raise ValueError("No model is configured. Please set up the Azure or Ollama model in the sidebar.")


def create_agent_executor():
    tools = load_tools(
        [],
    )
    return AgentExecutor(
        agent=create_react_agent(
            llm=get_model(),
            tools=tools,
            prompt=hub.pull("hwchase17/react"),
        ),
        tools=tools,
        max_iterations=3,
        handle_parsing_errors=True,
        verbose=True,
    )


if "messages" not in st.session_state:
    # default initial message to render in message state
    st.session_state["messages"] = [AIMessage(content="How can I help you?")]

# Loop through all messages in the session state and render them as a chat on every st.refresh mech
for msg in st.session_state.messages:
    # https://docs.streamlit.io/develop/api-reference/chat/st.chat_message
    # we store them as AIMessage and HumanMessage as its easier to send to LangGraph
    if isinstance(msg, AIMessage):
        st.chat_message("assistant").write(msg.content)
    if isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)

if prompt := st.chat_input():
    st.session_state.messages.append(HumanMessage(content=prompt))
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        msg_placeholder = st.empty()
        st_callback = get_streamlit_cb(st.empty())
        if agent == "react":
            response = create_agent_executor().invoke(
                {
                    "input": prompt,
                },
                {
                    "callbacks": [
                        st_callback,
                    ],
                },
            )
            last_msg = response["output"]
        elif agent == "basic_langgraph":
            graph = BasicAgent(
                llm=get_model(),
                tools=get_tools(),
            ).create_graph()
            response = invoke_graph(
                graph=graph,
                st_messages=st.session_state.messages,
                callables=[
                    st_callback,
                ],
            )
            last_msg = response["messages"][-1].content
        st.session_state.messages.append(AIMessage(content=last_msg))
        msg_placeholder.write(last_msg)
