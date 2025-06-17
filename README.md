
# GitHub User Activity CLI

A Python command-line tool that fetches and displays a GitHub user's recent activity using the GitHub API.

## Features

- Fetches recent activity for any public GitHub user
- Displays activities in a human-readable format
- Handles various event types (pushes, issues, stars, etc.)
- Graceful error handling for invalid usernames/API issues
- No external dependencies (except `requests`)

## Prerequisites

- Python 3.6 or higher
- `pip` package manager
- Internet connection (to access GitHub API)

Project URL: https://roadmap.sh/projects/github-user-activity

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/github-user-activity-cli.git
   cd github-user-activity-cli
   ```

2. Install the required dependency:
   ```bash
   pip install requests
   ```

## Usage

### Basic Usage
```bash
python github_activity.py <username>
```

Example:
```bash
python github_activity.py torvalds
```

### Expected Output
```
Fetching GitHub activity for torvalds...

Recent activity for torvalds:

- Pushed 2 commits to torvalds/linux (on May 15, 2023 at 14:30)
- Opened issue 'Kernel regression in 5.15' in torvalds/linux (on May 14, 2023 at 09:45)
- Starred git/git (on May 12, 2023 at 11:20)
```

### Rate Limiting Note
The GitHub API has rate limits (60 requests/hour for unauthenticated requests). If you hit the limit, you'll see:
```
Error fetching data: 403 Client Error: rate limit exceeded
```

## Advanced Options

### Using a GitHub Token (Recommended)
For higher rate limits (5000 requests/hour):

1. Create a personal access token:  
   https://github.com/settings/tokens (no special permissions needed)

2. Set it as environment variable:
   ```bash
   export GITHUB_TOKEN='your_token_here'
   ```

3. The script will automatically use it if available

### Output Formatting
You can pipe the output to a file:
```bash
python github_activity.py torvalds > activity_log.txt
```

## Error Handling

The tool handles common errors:
- Invalid username: `Error: User 'nonexistentuser' not found on GitHub.`
- Rate limit exceeded: `Error fetching data: 403 Client Error: rate limit exceeded`
- Connection issues: `Error fetching data: Failed to establish connection`

## Development

### Running Tests
```bash
python -m unittest discover tests
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License
MIT License - See [LICENSE](LICENSE) file for details
