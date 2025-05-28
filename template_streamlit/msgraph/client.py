from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient

from template_streamlit.msgraph.settings import Settings


class Client:
    def __init__(
        self,
        settings: Settings,
    ):
        self.graph_service_client = GraphServiceClient(
            credentials=ClientSecretCredential(
                client_id=settings.azure_client_id,
                tenant_id=settings.azure_tenant_id,
                client_secret=settings.azure_client_secret,
            ),
            scopes=settings.microsoft_graph_user_scopes.split(","),
        )

    async def get_users(self):
        """Get users from Microsoft Graph."""
        try:
            return await self.graph_service_client.users.get()
        except Exception as e:
            raise Exception(f"Error fetching users: {e}")

    async def get_calendar_events(self, user_id: str):
        """Get calendar events for a specific user."""
        try:
            return await self.graph_service_client.users.by_user_id(user_id).calendar.events.get()
        except Exception as e:
            raise Exception(f"Error fetching calendar events for user {user_id}: {e}")
