import sys
import requests
import json
from datetime import datetime

### Fetches the user's activity from GitHub API

def fetch_user_activity(username):
    url = f"https://api.github.com/users/{username}/events"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            print(f"Error: User '{username}' not found on GitHub.")
        else:
            print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Error fetching data: {err}")
    return None


### Parses the raw activity data into readable messages

def parse_activity(events):
    if not events:
        return []
    
    activity_messages = []
    
    for event in events:
        event_type = event.get('type')
        repo_name = event.get('repo', {}).get('name', 'unknown repository')
        created_at = event.get('created_at', '')
        
        # Format date
        try:
            date_obj = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
            formatted_date = date_obj.strftime("%b %d, %Y at %H:%M")
        except (ValueError, TypeError):
            formatted_date = "an unknown time"
        
        payload = event.get('payload', {})
        
        if event_type == "PushEvent":
            commits = payload.get('commits', [])
            commit_count = len(commits)
            if commit_count == 1:
                message = f"Pushed 1 commit to {repo_name}"
            else:
                message = f"Pushed {commit_count} commits to {repo_name}"
        
        elif event_type == "IssuesEvent":
            action = payload.get('action', 'did something with an issue')
            issue = payload.get('issue', {})
            issue_title = issue.get('title', 'untitled issue')
            message = f"{action.capitalize()} issue '{issue_title}' in {repo_name}"
        
        elif event_type == "PullRequestEvent":
            action = payload.get('action', 'did something with a pull request')
            pr = payload.get('pull_request', {})
            pr_title = pr.get('title', 'untitled pull request')
            message = f"{action.capitalize()} pull request '{pr_title}' in {repo_name}"
        
        elif event_type == "WatchEvent":
            message = f"Starred {repo_name}"
        
        elif event_type == "ForkEvent":
            forkee = payload.get('forkee', {}).get('html_url', 'a repository')
            message = f"Forked {repo_name} to {forkee}"
        
        elif event_type == "CreateEvent":
            ref_type = payload.get('ref_type', 'repository')
            message = f"Created a {ref_type} in {repo_name}"
        
        else:
            message = f"Performed {event_type} on {repo_name}"
        
        activity_messages.append(f"- {message} (on {formatted_date})")
    
    return activity_messages


### Displays the user's activity in the terminal

def display_activity(username, activities):
    if not activities:
        print(f"No recent activity found for {username} or the account is private.")
        return
    
    print(f"\nRecent activity for {username}:\n")
    for activity in activities[:10]:  # Show only the 10 most recent activities
        print(activity)
    print("\n")


### Main function to handle command line arguments and execute the program

def main():
    if len(sys.argv) != 2:
        print("Usage: python github_activity.py <username>")
        sys.exit(1)
    
    username = sys.argv[1]
    print(f"\nFetching GitHub activity for {username}...\n")
    
    raw_activity = fetch_user_activity(username)
    if raw_activity is None:
        sys.exit(1)
    
    parsed_activity = parse_activity(raw_activity)
    display_activity(username, parsed_activity)

if __name__ == "__main__":
    main()