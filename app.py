import json
import tempfile
from contextlib import suppress
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

default_print_options = {
    "paperWidth": 8.27,
    "paperHeight": 11.69,
    "displayHeaderFooter": False,
}


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

    print_options = dict(default_print_options)
    if isinstance(params.get("print_options"), dict):
        print_options.update(params.get("print_options"))

    pdf = generate_pdf(source, print_options)

    return {
        "statusCode": 201,
        "headers": {"Content-Type": "application/pdf"},
        "body": pdf,
        "isBase64Encoded": True,
    }


def generate_pdf(html: str, print_options) -> str:
    with tempfile.NamedTemporaryFile(prefix="/tmp/", suffix=".html") as tmp:
        tmp.write(html.encode())
        tmp.seek(0)

        driver = build_driver()
        driver.get("file://{}".format(tmp.name))

        pdf = driver.execute_cdp_cmd("Page.printToPDF", print_options)["data"]
        driver.quit()

        return pdf


def build_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--single-process")
    return webdriver.Chrome(options=options)
