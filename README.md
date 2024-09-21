# Continuous Integration (CI) Server

A Python-based Continuous Integration server that currently only supports running [Playwright](https://playwright.dev/) tests, triggered by pull requests to connected GitHub repositories. The server receives webhooks from GitHub, sets a pending status on the pull request, clones the repository, runs tests, and reports back the status to the specific pull request using the GitHub API. It also keeps log files so that users can view and debug directly via the pull request using the link for the current run check.

## Features

- **Automated Testing**: Automatically runs Playwright tests when a pull request is made.
- **GitHub Integration**: Seamlessly integrates with GitHub using webhooks and the GitHub API.
- **Status Updates**: Sets a pending status on the pull request while tests are running, and a status based on the output of the test execution.
- **Detailed Logging**: Maintains log files for each test run, accessible via the pull request.
- **Easy Debugging**: Provides direct links to logs for easy debugging within the pull request.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [License](#license)

## Installation

### Prerequisites

- See requirements.txt

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/ci-server.git
   cd ci-server
   ```
2. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up Environment Variables**
    ```js
    GITHUB_TOKEN_<NAME>=your_github_token
    SECRET_KEY<NAME>=your_webhook_secret
    ```
- `GITHUB_TOKEN_<NAME>`: A GitHub Personal Access Token with permissions to set statuses on pull requests.
- `SECRET_KEY_<NAME>`: A secret key to verify webhook payloads from GitHub.
- Replace \<NAME> with your app name

4. **Configure Github Webhook**
- Go to your GitHub repository's Settings > Webhooks > Add webhook.
- Payload URL: http://yourserver.com/build/\<NAME> (replace <NAME> with the same app name, and the placeholder base url with your domain for the hosted CI server).
- Content type: application/json.
- Secret: The SECRET_KEY_\<NAME> from your .env file.
- Events: Select `Let me select individual events` and check `Pull requests.`

5. **Run the server**
    ```bash
    cd src/
    python app.py
    ```


## Usage
Once the server is running and the webhook is configured, the CI pipeline will automatically trigger on pull requests.

- On Pull Request:
    -  The server receives a webhook from GitHub.
    - Sets the pull request status to pending.
    - Clones the repository to a local directory.
    - Executes Playwright tests located in the tests/ directory.
    - Updates the pull request status to success or failure based on test results.
    - Stores logs in the logs/ directory and provides a link in the pull request for debugging.


## Project Structure
```bash
src/
├── app.py                 # Flask app entry point
├── build/
│   └── server.py          # Main server functions (status updates, cloning, logging)
├── logs/                  # Folder for log files
├── parse_payload.py       # Parses the webhook payload from GitHub
└── utils/
    ├── run_tests.py       # Runs tests after the repository is cloned
    └── utils.py           # Utility functions (cloning/removing repos, verifying webhooks)
```

## License
This project is licensed under the [MIT License](https://opensource.org/license/mit).