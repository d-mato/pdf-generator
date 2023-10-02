# PDF-Generator

## API Spec

Example request:

```json
{
  "source": "<b>Hello World</b>",
  "print_options": {
    "pageSize": "A4"
  }
}
```

Response is Base64-encoded.

## Build

```sh
docker build -t pdf-generator .
```

## Run

```sh
docker run --rm -p 8000:5000 pdf-generator
```

Request:

```sh
curl -d '{"source":"<b>Hello World</b>"}' -H 'Content-Type: application/json' localhost:8000 > output.pdf
```

## Deploy to Lambda

```sh
cd terraform
terraform apply
```

## Test

```sh
python -m unittest
```
