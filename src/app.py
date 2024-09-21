from flask import Flask
from build.server import build_application


app = Flask(__name__)

app.add_url_rule('/build/<name>', 'build', build_application, methods=['POST'])

#TODO Add logging

if __name__ == "__main__":
    app.run(debug=True, port=8080)