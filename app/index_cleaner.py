from elasticsearch import Elasticsearch
from argparse import ArgumentParser
from environs import Env
import datetime
import requests
import time
import re


env = Env()
env.read_env()
ILM = env.dict('ILM', subcast=str)
# exp. ILM = {'1capache': '30', 'k8s-dev': '5', 'k8s-dev-ingress': '5', 'telegram-bot': '15', 'k8s-production': '30', 'syslog-production': '15', 'k8s-dev-feature': '5', 'k8s-production-ingress': '35', 'nginx-access-log': '35', '1c': '180', '1c-http_tsd': '90'}


def current_timestamp():
    return time.time()


def extract_timestamp(index):
    rex = r'(\d{4}[/.-]{0,1}\d{2}[/.-]{0,1}\d{2}$)'
    data = re.split(rex, index)
    if len(data) > 1:
        date = data[1].replace(".", "")
        # print(data[0][:-1], "     ", data[1], date)
        return time.mktime(datetime.datetime.strptime(date, "%Y%m%d").timetuple())


def get_time_diff(index):
    indic_timestamp = extract_timestamp(index)
    if indic_timestamp:
        timestamp = current_timestamp()
        diff_days = round((timestamp - indic_timestamp)/86400)
        return diff_days


def get_indices(host, port):
    _es = None
    _es = Elasticsearch([{'host': host, 'port': port}])
    if _es.ping():
        return _es.indices.get_alias("*")


def remove_index(host, port, name):
    assert name, 'you must set the index name for remove'
    uri = '/{}'.format(name)
    # print(uri)
    req = 'http://{h}:{p}{u}'.format(h=host, p=port, u=uri)
    # print(req)
    r = requests.delete(req,  timeout=60)
    return r.json()


def get_ilm(indic):
    # print(indic)
    # print(ILM)
    try:
        days = int(ILM[indic])
        if days > 0:
            # print(days)
            return days
    except Exception:
        rex = r'([-].[a-zA-Z0-9_.]*$)'
        data = re.split(rex, indic)
        if len(data) > 1:
            return get_ilm(data[0])
        else:
            return 1000


def main():
    p = ArgumentParser()
    p.add_argument('--host', required=True)
    p.add_argument('--port', required=True)
    p.add_argument('--debug', action='store_true')
    args = p.parse_args()

    list_indices = get_indices(args.host, args.port)
    for index in list_indices:
        if index[0] == ".":
            continue
        diff = get_time_diff(index)
        if diff:
            print("Index %s was created %d ago" % (index, diff))
            term_life = get_ilm(index)
            if diff > term_life:
                print("     Index %s will be removed, cause older %d days" % (index, term_life))
        

main()
