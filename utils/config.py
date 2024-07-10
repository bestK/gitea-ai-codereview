import os
from dotenv import load_dotenv


class Config:
    def __init__(self, config_file=None):
        load_dotenv(config_file)

        self.gitea_token: str = os.getenv("GITEA_TOKEN")
        self.gitea_host: str = os.getenv("GITEA_HOST")
        self.openai_key: str = os.getenv("OPENAI_KEY")
        self.copilot_token: str = os.getenv("COPILOT_TOKEN")
        self.ignored_file_suffix: str = os.getenv("IGNORED_FILE_SUFFIX")
        webhook: Webhook = Webhook()
        webhook.url = os.getenv("WEBHOOK_URL")
        webhook.header_name = os.getenv("WEBHOOK_HEADER_NAME")
        webhook.header_value = os.getenv("WEBHOOK_HEADER_VALUE")
        webhook.request_body = os.getenv("WEBHOOK_REQUEST_BODY")
        self.webhook = webhook
        self._validate()

    def _validate(self):
        if not self.gitea_token:
            raise ValueError("GITEA_TOKEN is required")
        if not self.gitea_host:
            raise ValueError("GITEA_HOST is required")
        if not self.copilot_token:
            raise ValueError("COPILOT_TOKEN is required")


class Webhook:
    def __init__(self):
        self.url: str = None
        self.header_name: str = None
        self.header_value: str = None
        self.request_body: str = None

    @property
    def is_init(self) -> bool:
        return self.url and self.request_body
