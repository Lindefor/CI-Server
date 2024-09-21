import os
import datetime
from flask import abort, jsonify


def get_all_logs():
    """
    Get all logs from the logs directory.
    """

    log_files = os.listdir("logs/")
    log_ids = [file[:-4] for file in log_files if file.endswith('.log')]

    return {"ids": log_ids}

def get_log(id: str):
    """
    Get the log with the specified ID.
    """

    log_file = f"logs/{id}.log"

    if not os.path.exists(log_file):
        abort(404)

    log_modified_date = datetime.datetime.fromtimestamp(os.path.getmtime(log_file)).isoformat()

    with open(log_file, 'r') as file:
        log_content = file.read()

    html_content = f"""
    <html>
    <head>
        <title>Log Details</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
            }}
            h1 {{
                color: #333;
            }}
            pre {{
                background-color: #f5f5f5;
                padding: 10px;
                border-radius: 5px;
                overflow: auto;
            }}
        </style>
    </head>
    <body>
        <h1>Log Details</h1>
        <h2>Commit ID: {id}</h2>
        <h3>Last Modified Date: {log_modified_date}</h3>
        <pre>{log_content}</pre>
    </body>
    </html>
    """

    return html_content
    # return jsonify({"commit": id, "log": log_content, "date": log_modified_date})

