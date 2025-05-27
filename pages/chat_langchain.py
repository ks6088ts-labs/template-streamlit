from logging import getLogger
from os import getenv

import streamlit as st
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_openai import AzureChatOpenAI
from openai import APIConnectionError, APIStatusError, APITimeoutError

load_dotenv(override=True)
logger = getLogger(__name__)

with st.sidebar:
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
        stream_mode = st.checkbox(
            label="ストリーム出力を有効にする",
            value=True,
            key="AZURE_OPENAI_STREAM_MODE",
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
        stream_mode = st.checkbox(
            label="ストリーム出力を有効にする",
            value=True,
            key="OLLAMA_STREAM_MODE",
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
        )
    elif is_ollama_configured():
        return ChatOllama(
            model=st.session_state.get("OLLAMA_MODEL", ""),
            temperature=0.0,
        )
    raise ValueError("No model is configured. Please set up the Azure or Ollama model in the sidebar.")


st.title("chat app with LangChain SDK")

if not is_configured():
    st.warning("Please fill in the required fields at the sidebar.")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "Hello! I'm a helpful assistant.",
        }
    ]

# Show chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Receive user input
if prompt := st.chat_input(disabled=not is_configured()):
    model = get_model()

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking..."):
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            try:
                if stream_mode:
                    # ストリーム出力
                    for chunk in model.stream(
                        input=[
                            {
                                "role": m["role"],
                                "content": m["content"],
                            }
                            for m in st.session_state.messages
                        ]
                    ):
                        if chunk.content is not None:
                            full_response += chunk.content
                            message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                else:
                    # 一括出力
                    response = model.invoke(
                        input=[
                            {
                                "role": m["role"],
                                "content": m["content"],
                            }
                            for m in st.session_state.messages
                        ]
                    )
                    full_response = response.content if hasattr(response, "content") else str(response)
                    message_placeholder.markdown(full_response)

                st.session_state.messages.append({"role": "assistant", "content": full_response})

            except APITimeoutError as e:
                logger.exception(f"APIタイムアウトエラーが発生しました: {e}")
                st.error(f"APIタイムアウトエラーが発生しました: {e}")
                st.warning("再度お試しいただくか、接続を確認してください。")
            except APIConnectionError as e:
                logger.exception(f"API接続エラーが発生しました: {e}")
                st.error(f"API接続エラーが発生しました: {e}")
                st.warning("ネットワーク接続を確認してください。")
            except APIStatusError as e:
                logger.exception(f"APIステータスエラーが発生しました: {e.status_code} - {e.response}")
                st.error(f"APIステータスエラーが発生しました: {e.status_code} - {e.response}")
                st.warning("Azure OpenAIの設定（デプロイメント名、APIバージョンなど）を確認してください。")
            except Exception as e:
                logger.exception(f"予期せぬエラーが発生しました: {e}")
                st.error(f"予期せぬエラーが発生しました: {e}")
