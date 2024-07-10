import re
import requests

from utils import logger


class GiteaClient:
    def __init__(self, host: str, token: str):
        self.host = host
        self.token = token

    def get_diff_blocks(self, owner: str, repo: str, sha: str) -> str:
        # Get the diff of the commit
        endpoint = f"https://{self.host}/api/v1/repos/{owner}/{repo}/git/commits/{sha}.diff?access_token={self.token}"
        res = requests.get(endpoint)
        if res.status_code == 200 and res.text != "":
            diff_blocks = re.split("diff --git ", res.text.strip())
            # 去掉空字符串
            diff_blocks = [block for block in diff_blocks if block]
            # 移除 'diff --git ' 前缀
            diff_blocks = [block.replace("diff --git ", "") for block in diff_blocks]
            return diff_blocks
        else:
            logger.error(f"Failed to get diff content: {res.text}")
            return None

    def create_issue(
        self, owner: str, repo: str, title: str, body: str, ref: str, pusher: str
    ):
        endpoint = f"https://{self.host}/api/v1/repos/{owner}/{repo}/issues?access_token={self.token}"
        data = {
            "assignee": "jenkins",
            "assignees": [pusher],
            "body": body,
            "closed": False,
            "due_date": None,
            "labels": [0],
            "milestone": 0,
            "ref": ref,
            "title": title,
        }
        res = requests.post(endpoint, json=data)
        if res.status_code == 201:
            return res.json()
        else:
            return None

    def add_issue_comment(self, owner, repo, issue_id, comment):
        endpoint = f"https://{self.host}/api/v1/repos/{owner}/{repo}/issues/{issue_id}/comments?access_token={self.token}"
        data = {
            "body": comment,
        }
        res = requests.post(endpoint, json=data)
        if res.status_code == 201:
            return res.json()
        else:
            return None

    def extract_info_from_request(request_body):
        full_name = request_body["repository"]["full_name"].split("/")
        owner = full_name[0]
        repo = full_name[1]
        sha = request_body["after"]

        ref = request_body["ref"]
        pusher = request_body["pusher"]["login"]
        full_name = request_body["pusher"]["full_name"]
        title = request_body["commits"][0]["message"]
        commit_url = request_body["commits"][0]["url"]

        return owner, repo, sha, ref, pusher, full_name, title, commit_url
