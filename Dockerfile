FROM python:slim

RUN apt update && apt install -y chromium chromium-driver

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY core.py .
COPY app.py .

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
