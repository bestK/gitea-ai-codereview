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


def create_comment(file_name: str, diff_content: str, response: str) -> str:
    return f"文件名：{file_name} \n\r 文件变更:\n\r ``` \n\r{diff_content} \n\r ``` \n\r ## 审查结果：\n\r {response}"
