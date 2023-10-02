from flask import Flask, request
import base64

from core import build_print_options, generate_pdf


app = Flask(__name__)


@app.post("/")
def index():
    try:
        params = request.json
    except Exception:
        params = {}

    source = params.get("source")
    if source is None:
        return {"error": "source is required"}, 400

    if isinstance(params.get("print_options"), dict):
        print_options = build_print_options(params.get("print_options"))
    else:
        print_options = build_print_options()

    pdf = generate_pdf(source, print_options)

    return base64.b64decode(pdf), 201
