FROM registry.company.com/python:3.8-slim-buster
WORKDIR /app
COPY ./app /app
RUN pip install --no-cache-dir -r requirements.txt
CMD python index_cleaner.py --host logs-es01.infra.company.local --port 9200 --debug