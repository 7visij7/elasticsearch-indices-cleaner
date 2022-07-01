FROM registry.puls.ru/python:3.8-slim-buster
WORKDIR /app
COPY ./app /app
RUN pip install --no-cache-dir -r requirements.txt
CMD python index_cleaner.py --host logs-es02.infra.puls.local --port 9200 --debug