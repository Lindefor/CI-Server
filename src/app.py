from flask import Flask
from build.server import build_application
from logs.logs import get_all_logs, get_log


app = Flask(__name__)

app.add_url_rule('/build/<string:name>', 'build', build_application, methods=['POST'])
app.add_url_rule('/logs/all', 'logs_all', get_all_logs, methods=['GET'])
app.add_url_rule('/logs/<string:id>', 'logs', get_log, methods=['GET'])


if __name__ == "__main__":
    app.run(port=8024)