import requests
import datetime
import os

# Retrieve the GitHub personal access token from the secret
github_token = os.environ.get("MY_TOKEN")

# Ensure the token is available
if github_token is None:
    raise ValueError("GitHub personal access token not found in secrets.")

# Set the API endpoint and user information
api_endpoint = "https://api.github.com"
username = "jankigabani"
repo_name = "Jankigabani"
readme_path = "README.md"

headers = {
    "Authorization": f"token {github_token}"
}

# Fetch the contents of the README file
readme_url = f"{api_endpoint}/repos/{username}/{repo_name}/contents/{readme_path}"
response = requests.get(readme_url)
readme_data = response.json()

# Decode the base64-encoded content
import base64
readme_text = base64.b64decode(readme_data["content"]).decode("utf-8")

# Find the comment section and check if the current date is already in it
today = datetime.date.today().strftime("%Y-%m-%d")
date_like_comment = f"<!-- {today} -->"
comment_start = "<!-- START_SECTION: daily-comment -->"
comment_end = "<!-- END_SECTION: daily-comment -->"

start_index = readme_text.find(comment_start)
end_index = readme_text.find(comment_end)

if start_index != -1 and end_index != -1:
    comment_section = readme_text[start_index + len(comment_start):end_index]
    if date_like_comment not in comment_section:
        new_comment = f"\n{date_like_comment}"
        new_readme_text = (
            readme_text[:end_index] + new_comment + readme_text[end_index:]
        )
        new_readme_content = base64.b64encode(new_readme_text.encode("utf-8")).decode("utf-8")

        # Update the README file with the new content
        commit_message = f"Update README.md"
        update_url = f"{api_endpoint}/repos/{username}/{repo_name}/contents/{readme_path}"
        update_data = {
            "message": commit_message,
            "content": new_readme_content,
            "sha": readme_data["sha"]
        }

        response = requests.put(update_url, headers=headers, json=update_data)

        if response.status_code == 200:
            print(f"Updated README with comment for {today}")
        else:
            print(f"Failed to update README. Status code: {response.status_code}")
    else:
        print(f"Comment for {today} already exists in the README")
else:
    print("Comment section not found in the README")
