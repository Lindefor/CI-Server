import json
from flask import abort, request
import requests
import os
import sys
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from parse_payload import Payload
from utils.utils import verify_webhook_signature, _clone_repo, _remove_repo
from utils.run_tests import run_tests

def start_logger(commit_sha: str):
    """
    Start a logger for the CI pipeline.

    :param commit_sha: The SHA of the commit.
    :type commit_sha: str

    :return: A logger object.
    :rtype: logging.Logger
    """
    log_path = os.path.join("logs", f"{commit_sha}.log")

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger

def set_status(commit_sha: str, state: str, description: str, target_url: str, repo_name: str, repo_owner: str, github_token: str) -> dict:
    """
    Set the status of a commit with the GitHub API.

    :param commit_sha: The SHA of the commit
    :type commit_sha: str

    :param state: The state of the status ("pending", "success", "error" or "failure")
    :type state: str

    :param description: Short description of the status, seen in GitHub.
    :type description: str

    :param target_url: This URL will be linked from GitHub for further information.
    :type target_url: str

    :param repo_name: The name of the repository.
    :type repo_name: str

    :param repo_owner: The owner of the repository.
    :type repo_owner: str

    :param github_token: Token with the required permissions.
    :type github_token: str

    :return: The response from the GitHub API.
    :rtype: dict
    """

    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/statuses/{commit_sha}"

    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github+json",
    }

    if target_url != "":
        data = {
            "state": state,
            "target_url": target_url,
            "description": description
        }
    else:
        data = {
            "state": state,
            "description": description
        }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()


def build_application(name: str):
    """
    Execute the build command. Currently only runs the tests and stores logs.

    This function is a Flask POST endpoint that receives an API call from GitHub webhooks

    :return: A tuple containing a message and a status code.
    :rtype: tuple
    """
    secret_env = 'BUILD_SECRET_' + name
    github_token_env = 'GITHUB_TOKEN_' + name 
    secret_message = os.getenv(secret_env)
    github_token = os.getenv(github_token_env)

    if not secret_message or not github_token:
        abort(400, "Secret message or GitHub token not found for specified project name")

    verified = verify_webhook_signature(request.data, secret_message, request.headers["X-Hub-Signature-256"])

    if not verified:
        abort(403, "x-hub-signature-256 header missing or invalid!")

    payload_data = request.json

    try:
        payload = Payload('pull_request', payload_data)
        action = payload.action
    except (KeyError, AttributeError) as error:
        print(error)
        abort(400, "Invalid payload")

    logger = start_logger(payload.commit_sha)
    target_url = request.url.replace(f"build/{name}", f"logs/{payload.commit_sha}")

    if action in ['opened', 'reopened', 'synchronize', 'edited']:
        set_status(payload.commit_sha, "pending", "Running tests", "", payload.repo_name, payload.repo_owner, github_token)

        logger.debug(f"Test suite started for commit {payload.commit_sha}")
        info = _clone_repo(payload.clone_url)
        repo_path, repo = info[0], info[1]
        logger.debug(f"Repository cloned to {repo_path}")

        repo.git.checkout(payload.commit_sha)
        logger.debug(f"Checked out commit {payload.commit_sha}")

        test_result_code = 1
        test_output = ""
        test_result_code, test_output = run_tests(repo_path)
        logger.info(f"Unit tests completed with code: {test_result_code}")
        logger.debug(f"Unit tests output: {test_output}")

        # Set success/failure status upon test/syntax completion
        if test_result_code == 0:
            set_status(payload.commit_sha, "success", "Build succeeded", target_url, payload.repo_name, payload.repo_owner, github_token)
            logger.info("Test suite completed successfully for commit {payload.commit_sha}")
        else:
            set_status(payload.commit_sha, "failure", "Build failed", target_url, payload.repo_name, payload.repo_owner, github_token)
            logger.error("Test suite failed for commit {payload.commit_sha}")

        _remove_repo(repo_path)

        logger.debug(f"Repository removed for commit {payload.commit_sha}")

    else:
        print("Closed or other action")

    return "Build command executed", 200