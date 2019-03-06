import os
import pandas as pd
import requests
import networkx as nx
import json
import sys, traceback
import multiprocessing
import time
from unshortenit import UnshortenIt
from tqdm import tqdm
import sqlite3
from urllib.parse import urlparse


def get_urls():
    """
    提取需要分析的URL
    """
    tweets = pd.read_csv('data/ira-tweets-ele.csv')
    print(len(tweets))

    for i, row in tweets.iterrows():
        # print(i, row, type(row), row['urls'], type(row['urls']))
        if not isinstance(row['urls'], str):
            # tweets.drop(i, inplace=True)
            pass
        elif row['urls'][1: -1] == '':
            # tweets.drop(i, inplace=True)
            pass
        else:
            try:
                url = row['urls'][1: -1]
                hostname = urlparse(url).hostname
                print(i, row["tweetid"], url, hostname, sep='\t')
            except Exception as e:
                # pass
                traceback.print_exc(file=sys.stdout)
                # print(i, e)


def task(_ids):
    print("{} task starts ... ".format(os.getpid()), len(_ids))
    unshortener = UnshortenIt(default_timeout=10)
    new_ids = []
    for d in tqdm(_ids):
        # if "error" in d and d["error"]:
        #     print(d)
        try:
            d["error"] = False
            url = unshortener.unshorten(d["url"])
            d["final_url"] = url
            hostname = urlparse(url).hostname
            d['hostname'] = hostname

        except Exception as e:
            d['error'] = True

        new_ids.append(d)
    write2json(new_ids)

    return new_ids


def get_hostname(_ids):
    new_ids = []
    for d in tqdm(_ids):
        url = d["final_url"]
        hostname = urlparse(url).hostname
        d['hostname'] = hostname
        new_ids.append(d)
    write2json(new_ids)

    return new_ids


def write2json(new_ids):
    print("writing ... ...")
    with open("data/ira-urls-last.json", "a") as f:
        for d in new_ids:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
    print("finished!")


def unshorten_url():
    dict_id_host = []
    for line in open('data/ira-id-url-ele.csv'):
        _id, tweetid, url, hostname = line.strip().split('\t')
        d = {
            'id': _id,
            'tweetid': tweetid,
            'url': url,
            'hostname': hostname,
            'final_url': url,
            'short': False
        }
        if len(hostname) <= 10:
            d['short'] = True
        dict_id_host.append(d)

    # task(dict_id_host)
    
    task_cnt = 8
    step = int(len(dict_id_host) / task_cnt)
    pool = multiprocessing.Pool()
    for i in range(task_cnt + 1):
        if i == task_cnt - 1:
            _ids = dict_id_host[i * step:]
        elif i < task_cnt:
            _ids = dict_id_host[i * step: (i + 1) * step]
        else:
            _ids = []
        
        pool.apply_async(task, (_ids,))

    pool.close()
    pool.join()


def again():
    dict_id_host = []
    
    # for line in open("ira-urls.json"):
    for line in open("ira-final-urls.json"):
        d = json.loads(line.strip())
        dict_id_host.append(d)

    # task(dict_id_host)
    get_hostname(dict_id_host)
    return 0

    """
    task_cnt = 6
    step = int(len(dict_id_host) / task_cnt)
    pool = multiprocessing.Pool()

    for i in range(task_cnt):
        if i == task_cnt - 1:
            _ids = dict_id_host[i * step:]
        else:
            _ids = dict_id_host[i * step: (i + 1) * step]
        
        pool.apply_async(task, (_ids,))

    pool.close()
    pool.join()
    """


if __name__ == "__main__":
    # get_urls()
    unshorten_url()
    # again()

