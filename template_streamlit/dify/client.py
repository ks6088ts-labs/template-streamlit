import uuid

import httpx

from template_streamlit.dify.settings import Settings


class Client:
    def __init__(
        self,
        settings: Settings,
    ):
        self.settings = settings

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.settings.dify_api_key}",
            "Content-Type": "application/json",
        }

    def workflows_run(self, inputs: dict):
        response = httpx.post(
            headers=self._get_headers(),
            url="https://api.dify.ai/v1/workflows/run",
            json={
                "inputs": inputs,
                "response_mode": "blocking",
                "user": uuid.uuid4().hex,
            },
            timeout=60 * 2,
        )
        response.raise_for_status()
        return response.json()
