FROM python:3.12-slim

WORKDIR /tests

COPY requirements.txt /tests/requirements.txt

RUN pip install --no-cache-dir -r /tests/requirements.txt

COPY . /tests

CMD ["pytest", "-q"]