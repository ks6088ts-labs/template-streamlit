from logging import getLogger
from os import getenv

import streamlit as st
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_openai.chat_models.base import BaseChatOpenAI
from openai import APIConnectionError, APIStatusError, APITimeoutError

load_dotenv()
logger = getLogger(__name__)

with st.sidebar:
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
    "[View the source code](https://github.com/ks6088ts-labs/template-streamlit/tree/main/apps/chat.py)"


def is_configured():
    return azure_openai_api_key and azure_openai_endpoint and azure_openai_api_version and azure_openai_gpt_model


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
    model: BaseChatOpenAI = AzureChatOpenAI(
        azure_endpoint=azure_openai_endpoint,
        api_key=azure_openai_api_key,
        openai_api_version=azure_openai_api_version,
        azure_deployment=azure_openai_gpt_model,
    )

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking..."):
        # アシスタントの応答を表示するためのプレースホルダー
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            # Azure OpenAIにストリームリクエストを送信
            try:
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
                        message_placeholder.markdown(full_response + "▌")  # カーソルを模倣
                message_placeholder.markdown(full_response)  # 最終的な応答

                # アシスタントの応答を履歴に追加
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
