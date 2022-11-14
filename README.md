# Elasticsearch-indices-cleaner
>The application cleans up old elasticsearch indexes according to ILM.

___
## Run application
> Install application requirements from [requirements.txt](https://github.com/7visij7/elasticsearch-indices-cleaner/tree/main/app) and run application.
```Bash
pip install --no-cache-dir -r app/requirements.txt
 
python app/index_cleaner.py --host $HOSTNAME --port $PORT --debug
```
+  $HOSTNAME and $PORT parametrs to connect to Elasticsearch cluster.

---

## Required variables

> Required enviroment variable ILM (indices life managmet), where store name of index and nubmers of days which index should stored. 
 
e.g.:
```Python
ILM = {'1capache': '30', 'k8s-dev': '5', 'k8s-dev-ingress': '5', 'telegram-bot': '15', 'k8s-production': '30', 'syslog-production': '15', 'k8s-dev-feature': '5', 'k8s-production-ingress': '35', 'nginx-access-log': '35', '1c': '180', '1c-http_tsd': '90'}
```

---
## Docker

> Build Docker image from a [Dockerfile](https://github.com/7visij7/elasticsearch-indices-cleaner/blob/main/Dockerfile)
```
docker build -t IMAGENAME
```
> Start application
```
docker run --rm IMAGENAME
```

---
## Kubernetes

> Deploy [Cronjob](https://github.com/7visij7/elasticsearch-indices-cleaner/blob/main/k8s/cronjob.yml) to kubernetes cluster.
```Bash
kubectl create namespace elasticsearch-indices-cleaner
kubectl apply -f k8s/cronjob.yml -n namespace elasticsearch-indices-cleaner
```