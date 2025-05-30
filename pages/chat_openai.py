from logging import getLogger
from os import getenv

import streamlit as st
from dotenv import load_dotenv
from openai import APIConnectionError, APIStatusError, APITimeoutError, AzureOpenAI

load_dotenv(override=True)
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
    stream_mode = st.checkbox(label="ストリーム出力を有効にする", value=True, key="AZURE_OPENAI_STREAM_MODE")
    "[Azure Portal](https://portal.azure.com/)"
    "[Azure OpenAI Studio](https://oai.azure.com/resource/overview)"
    "[View the source code](https://github.com/ks6088ts-labs/template-streamlit)"


def is_configured():
    return azure_openai_api_key and azure_openai_endpoint and azure_openai_api_version and azure_openai_gpt_model


st.title("chat app with OpenAI SDK")

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
    client = AzureOpenAI(
        api_key=azure_openai_api_key,
        api_version=azure_openai_api_version,
        azure_endpoint=azure_openai_endpoint,
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
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            try:
                if stream_mode:
                    # ストリーム出力
                    stream = client.chat.completions.create(
                        model=azure_openai_gpt_model,
                        messages=[
                            {
                                "role": m["role"],
                                "content": m["content"],
                            }
                            for m in st.session_state.messages
                        ],
                        stream=True,
                    )

                    for chunk in stream:
                        if len(chunk.choices) <= 0:
                            continue
                        if chunk.choices[0].delta.content is not None:
                            full_response += chunk.choices[0].delta.content
                            message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                else:
                    # 一括出力
                    response = client.chat.completions.create(
                        model=azure_openai_gpt_model,
                        messages=[
                            {
                                "role": m["role"],
                                "content": m["content"],
                            }
                            for m in st.session_state.messages
                        ],
                        stream=False,
                    )
                    # stream=False の場合は choices[0].message.content に全応答が入る
                    full_response = response.choices[0].message.content
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
