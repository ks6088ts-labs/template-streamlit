from langchain_openai import AzureChatOpenAI
from openai import AzureOpenAI

from template_streamlit.ai.settings import Settings


class Client:
    def __init__(
        self,
        settings: Settings,
    ):
        self.azure_openai = AzureOpenAI(
            api_key=settings.azure_openai_api_key,
            api_version=settings.azure_openai_api_version,
            azure_endpoint=settings.azure_openai_endpoint,
        )
        self.azure_chat_openai = AzureChatOpenAI(
            azure_endpoint=settings.azure_openai_endpoint,
            api_key=settings.azure_openai_api_key,
            openai_api_version=settings.azure_openai_api_version,
            azure_deployment=settings.azure_openai_gpt_model,
        )

    def get_azure_openai(self) -> AzureOpenAI:
        return self.azure_openai

    def get_azure_chat_openai(self) -> AzureChatOpenAI:
        return self.azure_chat_openai
