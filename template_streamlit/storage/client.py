from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

from template_streamlit.storage.settings import Settings


class Client:
    def __init__(
        self,
        settings: Settings,
        authentication_method: str = "CONNECTION_STRING",
    ):
        if authentication_method == "CONNECTION_STRING":
            self.blob_service_client = BlobServiceClient.from_connection_string(
                settings.azure_storage_connection_string,
            )
        elif authentication_method == "PASSWORDLESS":
            self.blob_service_client = BlobServiceClient(
                account_url=settings.azure_storage_account_url,
                credential=DefaultAzureCredential(),
            )
        if not self.blob_service_client:
            raise ValueError("Failed to create BlobServiceClient. Check your settings.")

    # Container Operations
    def create_container(self, container_name: str):
        return self.blob_service_client.create_container(container_name)

    def get_container_client(self, container_name: str):
        return self.blob_service_client.get_container_client(container_name)

    def delete_container(self, container_name: str):
        container_client = self.get_container_client(container_name)
        return container_client.delete_container()

    def list_containers(self):
        return self.blob_service_client.list_containers()

    # Blob Operations
    def upload_blob(self, container_name: str, blob_name: str, data):
        container_client = self.get_container_client(container_name)
        return container_client.upload_blob(blob_name, data)

    def download_blob(self, container_name: str, blob_name: str):
        container_client = self.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        return blob_client.download_blob().readall()

    def delete_blob(self, container_name: str, blob_name: str):
        container_client = self.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        return blob_client.delete_blob()

    def list_blobs(self, container_name: str):
        container_client = self.get_container_client(container_name)
        return container_client.list_blobs()
