import base64
import json
import tempfile
from contextlib import suppress
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


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

    pdf = generate_pdf(source)
    return {
        "headers": {"Content-Type": "application/pdf"},
        "body": pdf,
        "isBase64Encoded": True,
    }


def generate_pdf(html: str) -> str:
    with tempfile.NamedTemporaryFile(prefix="/tmp/", suffix=".html") as tmp:
        tmp.write(html.encode())
        tmp.seek(0)

        driver = build_driver()
        driver.get("file://{}".format(tmp.name))

        print_options = {
            "paperWidth": 8.27,
            "paperHeight": 11.69,
            "displayHeaderFooter": False,
        }
        return driver.execute_cdp_cmd("Page.printToPDF", print_options)["data"]


def build_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--single-process")
    return webdriver.Chrome(options=options)
