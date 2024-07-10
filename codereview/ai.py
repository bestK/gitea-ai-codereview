from abc import ABC, abstractmethod


class AI(ABC):
    @abstractmethod
    def code_review(self, diff_content: str, model: str) -> str:
        pass

    @abstractmethod
    def get_access_token(self) -> str:
        pass

    @abstractmethod
    def banner(self) -> str:
        pass
