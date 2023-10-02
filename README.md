# PDF-Generator

## Build

```sh
docker build -t pdf-generator .
```

## Run

```sh
docker run --rm -p 9000:8080 pdf-generator
```

Post event:

```sh
curl -d '{"body":"{\"source\":\"Hello World\"}"}' localhost:9000/2015-03-31/functions/function/invocations | jq -r .body | base64 -d > output.pdf
```

## Deploy

```sh
cd terraform
terraform apply
```

## Test

```sh
python -m unittest
```
