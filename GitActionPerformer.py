import requests
import datetime
import os  # Import the os module to access environment variables

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
readme_content = response.json()["content"]

# Decode the base64-encoded content
import base64
readme_text = base64.b64decode(readme_content).decode("utf-8")

# Find the comment section and check if the current date is already in it
today = datetime.date.today().strftime("%Y-%m-%d")
comment_start = "<!-- START_SECTION: daily-comment -->"
comment_end = "<!-- END_SECTION: daily-comment -->"
comment_section = readme_text[readme_text.index(comment_start):readme_text.index(comment_end)]
if today in comment_section:
    exit()

# Add the current date to the comment section
new_comment = f"\n- {today}"
new_readme_text = readme_text.replace(comment_section, f"{comment_section}\n{new_comment}")

# Encode the new README content
new_readme_content = base64.b64encode(new_readme_text.encode("utf-8")).decode("utf-8")

# Update the README file with the new content
commit_message = f"Update daily comment for {today}"
update_url = f"{api_endpoint}/repos/{username}/{repo_name}/contents/{readme_path}"
update_data = {
    "message": commit_message,
    "content": new_readme_content,
    "sha": response.json()["sha"]
}
response = requests.put(update_url, json=update_data)