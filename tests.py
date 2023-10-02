import json
import unittest
from unittest.mock import MagicMock, patch

from app import generate_pdf, handler

ENCODED_PDF = "TEST"


def MockChromeDriver(options=None):
    mock = MagicMock()
    mock.execute_cdp_cmd.return_value = {"data": ENCODED_PDF}
    return mock


@patch("app.webdriver", MagicMock(Chrome=MockChromeDriver))
class PdfGeneratorTest(unittest.TestCase):
    def test_handler(self):
        event = {
            "body": json.dumps(
                {
                    "source": "<b>Hello World</b>",
                    "print_options": {
                        "pageSize": "A4",
                    },
                }
            ),
        }
        res = handler(event, {})

        self.assertEqual(res["statusCode"], 201)
        self.assertEqual(res["body"], ENCODED_PDF)

    def test_handler_validation(self):
        event = {"body": json.dumps({})}
        res = handler(event, {})

        self.assertEqual(res["statusCode"], 400)

    def test_generate_pdf(self):
        pdf = generate_pdf("<b>Hello World</b>", {})

        self.assertEqual(pdf, ENCODED_PDF)
