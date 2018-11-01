import sqlite3
import json
import queue


def find_fake_tweets():
    host_label = json.load(open('data/host_label.json'))
    conn = sqlite3.connect("/home/alex/network_workdir/elections/databases/urls_db.sqlite")
    c = conn.cursor()
    c.execute('''SELECT * FROM urls;''')
    col_names = [t[0] for t in c.description]
    data = c.fetchall()

    with open("fake.txt", "w") as f:
        for i, d in enumerate(data):
            if i % 10000 == 0:
                print(i, d)
            if d[8] in host_label and host_label[d[8]] == "fake":
                json_d = {k: v for k, v in zip(col_names, d)}
                json_d = json.dumps(json_d, ensure_ascii=False)
                f.write(json_d + '\n')


def find_retweets(tweets_ids, out_name):
    q = set()
    new_nodes = set()
    for _id in tweets_ids:
        q.add(_id)

    dealed = set([])
    conn = sqlite3.connect("/home/alex/network_workdir/elections/databases_ssd/complete_trump_vs_hillary_db.sqlite")
    c = conn.cursor()

    cnt = 0
    edge_cnt = 0
    with open(out_name, "w") as f:
        while q:
            _id = q.pop()

            cnt += 1
            if cnt % 20000 == 0:
                # print(_id, _id in dealed)
                print('已经处理的点：', len(dealed), "；边的数量：", edge_cnt, "；等待处理队列：", len(q))
            dealed.add(_id)

            c.execute('''SELECT tweet_id FROM tweet_to_retweeted_uid WHERE retweet_id={};'''.format(_id))
            data = c.fetchall()

            for line in data:
                tid = line[0]
                edge_cnt += 1
                f.write("{}\t{}\n".format(_id, tid))
                if tid not in dealed:
                    new_nodes.add(tid)
                    # print("终于添加新点了！", len(q))
                    q.add(tid)
    print(len(new_nodes))

def load_all_nodes_v1():
    tweets_ids = set([])
    for line in open("data/retweet_network_1.txt"):
        n1, n2 = line.strip().split("\t")
        tweets_ids.add(int(n1))
        tweets_ids.add(int(n2))
    print(len(tweets_ids))

    t2 = set([int(json.loads(line.strip())["tweet_id"]) for line in open("data/fake.txt")])
    tweets_ids = tweets_ids | t2
    print(len(tweets_ids))
    return tweets_ids


def load_all_nodes():

    tweets_ids = set([int(json.loads(line.strip())["tweet_id"]) for line in open("data/fake.txt")])

    for line in open("data/retweet_network_1.txt"):
        n1, n2 = line.strip().split("\t")
        tweets_ids.add(int(n1))
        tweets_ids.add(int(n2))

    for line in open("data/retweet_network_2.txt"):
        n1, n2 = line.strip().split("\t")
        tweets_ids.add(int(n1))
        tweets_ids.add(int(n2))

    return tweets_ids


def union_retweet_line():
    retween_lines = set()
    for line in open("data/retweet_network_1.txt"):
        retween_lines.add(line)
    for line in open("data/retweet_network_2.txt"):
        retween_lines.add(line)
    with open("data/edge-tid-fake-news.txt", "w") as f:
        for line in retween_lines:
            f.write(line)


if __name__ == "__main__":
    tweets_ids = set([json.loads(line.strip())["tweet_id"] for line in open("data/fake.txt")])
    # tweets_ids = load_all_nodes_v1()
    find_retweets(tweets_ids, "data/retweet_network_1.txt")

    # union
    # tweets_ids = load_all_nodes()
    # with open("data/node-tid-fake-news.txt", "w") as f:
    #     for tid in tweets_ids:
    #         f.write(str(tid) + "\n")

    # union_retweet_line()