import os
from dotenv import load_dotenv, set_key
import requests
from codereview.ai import AI
from loguru import logger


class Copilot(AI):
    def __init__(self, copilot_token: str):
        if copilot_token is None or copilot_token == "":
            raise ValueError("copilot_token is required")

        self.copilot_token = copilot_token
        self.access_token = self.get_access_token()

    def code_review(self, diff_content: str, model: str = "gpt-4-0125-preview") -> str:
        """
        Perform code review using Copilot AI.

        Args:
            diff_content (str): The content of the code diff.

        Returns:
            None
        """

        # Set the URL of the OpenAI API endpoint

        url = "https://api.cocopilot.org/chat/completions"

        # Set the HTTP headers for the API request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
            "editor-version": "vscode/1.91.0",
            "editor-plugin-version": "copilot-chat/0.16.1",
        }

        # Set the data for the API request
        data = {
            "messages": [
                {
                    "role": "system",
                    "content": 'You are an AI programming assistant.\nWhen asked for your name, you must respond with "GitHub Copilot".\nFollow the user\'s requirements carefully & to the letter.\nFollow Microsoft content policies.\nAvoid content that violates copyrights.\nIf you are asked to generate content that is harmful, hateful, racist, sexist, lewd, violent, or completely irrelevant to software engineering, only respond with "Sorry, I can\'t assist with that."\nKeep your answers short and impersonal.\nYou can answer general programming questions and perform the following tasks: \n* Ask a question about the files in your current workspace\n* Explain how the code in your active editor works\n* Review the selected code in your active editor\n* Generate unit tests for the selected code\n* Propose a fix for the problems in the selected code\n* Scaffold code for a new workspace\n* Create a new Jupyter Notebook\n* Find relevant code to your query\n* Propose a fix for the a test failure\n* Ask questions about VS Code\n* Generate query parameters for workspace search\n* Ask about VS Code extension development\n* Ask how to do something in the terminal\n* Explain what just happened in the terminal\nYou use the GPT-4 Turbo version of OpenAI\'s GPT models.\nFirst think step-by-step - describe your plan for what to build in pseudocode, written out in great detail.\nThen output the code in a single code block.\nMinimize any other prose.\nUse Markdown formatting in your answers.\nMake sure to include the programming language name at the start of the Markdown code blocks.\nAvoid wrapping the whole response in triple backticks.\nThe user works in an IDE called Visual Studio Code which has a concept for editors with open files, integrated unit test support, an output pane that shows the output of running the code as well as an integrated terminal.\nThe user is working on a Windows machine. Please respond with system specific commands if applicable.\nThe active document is the source code the user is looking at right now.\nYou can only give one reply for each conversation turn.\nRespond in the following locale: zh-cn',
                },
                {
                    "role": "user",
                    "content": f"{diff_content} Code review",
                },
            ],
            "model": model,
            "max_tokens": 4096,
            "temperature": 0.1,
            "top_p": 1,
            "n": 1,
            "stream": False,
        }

        # Process the API response
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 401:
            openai_key = self.get_access_token(renew=True)
            self.access_token = openai_key
            return self.code_review(diff_content, model)

        if response.status_code == 200:
            messages = response.json()["choices"][0]["message"]["content"]
            return messages
        else:
            logger.error(f"get_openai_chat_response has error:{response.text}")
            return response.text

    def get_access_token(self, renew: bool = False) -> str:
        if not renew:
            load_dotenv()
            openai_key = os.getenv("OPENAI_KEY")
            logger.info(
                f"Using existing OpenAI key:{openai_key}",
            )
            return openai_key

        endpoint = "https://api.cocopilot.org/copilot_internal/v2/token"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"token {self.copilot_token}",
            "editor-version": "vscode/1.91.0",
            "editor-plugin-version": "copilot-chat/0.16.1",
        }
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            openai_key = response.json()["token"]
            set_key(".env", "OPENAI_KEY", openai_key)
            logger.success(f"Updated OpenAI key:{openai_key}")
            return openai_key
        else:
            logger.error("Failed to get OpenAI key", response.text)
            raise Exception("Failed to get OpenAI key")

    @property
    def banner(self) -> str:
        return "## Power by \n ![GitHub_Copilot_logo](/attachments/c99d46b9-d26f-4859-ad4f-d77650b27f8e)"
