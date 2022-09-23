import base64
import json
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def handler(event, context):
    body = json.loads(event["body"])
    source = body.get("source")

    if source is None:
        return {"statusCode": 400, "body": json.dumps({"error": "source is required"})}

    pdf = generate_pdf(source)
    return {
        "headers": {"Content-Type": "application/pdf"},
        "body": pdf.decode("utf-8"),
        "isBase64Encoded": True,
    }


def generate_pdf(html: str) -> bytes:
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
        pdf_base64 = driver.execute_cdp_cmd("Page.printToPDF", print_options)
        return base64.b64decode(pdf_base64["data"])


def build_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(options=options)