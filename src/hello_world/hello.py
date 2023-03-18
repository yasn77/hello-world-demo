"""Simple Flask app that prints Hello World or Hello <name>"""
from flask import Flask, request, jsonify
from markupsafe import escape

app = Flask(__name__)


def output(name, outf='string'):
    """Method to return either string or JSON output"""
    ret = ""
    escaped = escape(name.title())
    if outf == 'json':
        ret = jsonify({"output": f"Hello, {escaped}!", "name": escaped})
    else:
        ret = f"Hello, {escaped}!"
    return ret


@app.route('/')
def hello():
    """/ endpoint that prints Hello, World"""
    outf = request.args.get('output', default="string")
    return output("World", outf)


@app.route('/hello/<name>')
def hello_name(name):
    """Endpoint that takes name and returns Hello <name>"""
    outf = request.args.get('output', default="string")
    return output(name, outf)


if __name__ == '__main__':
    app.run()
