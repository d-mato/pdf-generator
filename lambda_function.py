import json
from contextlib import suppress

from core import build_print_options, generate_pdf


def handler(event, context):
    params = {}
    with suppress(Exception):
        parsed = json.loads(event["body"])
        params = parsed if isinstance(parsed, dict) else {}

    source = params.get("source")
    if source is None:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "source is required"}),
        }

    if isinstance(params.get("print_options"), dict):
        print_options = build_print_options(params.get("print_options"))
    else:
        print_options = build_print_options()

    pdf = generate_pdf(source, print_options)

    return {
        "statusCode": 201,
        "headers": {"Content-Type": "application/pdf"},
        "body": pdf,
        "isBase64Encoded": True,
    }
