#-*- coding: utf-8 -*-

"""
Created on 2018-12-01 17:02:07
@author: https://kayzhou.github.io/
"""
from my_weapon import *
from SQLite_handler import find_tweet


class URL_TWEET:
    """
    1. 根据URL获取传播fake news的tweets；(fake-tweets.json)
    2. 若转发了之上tweets，则添加到url_tweets中；(属于key则说明是转发推特，retweet_network_fake.json)
    3. 将IRAs数据中的存在于选举时间且包括相关关键词的数据筛选出，若URL为fake news则添加到url_tweets中；IRAs = True
    4. 若IRAs数据中转发了智商tweets，则添加到url_tweets中；IRA = True
    5. 整理数据结构，URL为key；
    6. url_tweets中tweets按时间排序；

    每行必要数据：tweet_id, user_id, dt, first, source, URL, hostname, IRA
    """
    def __init__(self):
        self.url_tweets = {}
        # self.set_tweets = set()

    def fill_url_tweets(self):
        for line in tqdm(open("data/fake_tweets_mbfc.json")):
            d = json.loads(line)
            if "final_url" in d:
                tweet = {
                    "tweet_id": str(d["tweet_id"]),
                    "user_id": str(d["user_id"]),
                    "dt": d["datetime_EST"],
                    "is_first": -1,
                    "is_source": -1,
                    "is_IRA": -1,
                    "URL": d["final_url"].lower(),
                    "hostname": d["final_hostname"].lower()
                }
                self.url_tweets[str(d["tweet_id"])] = tweet


    def file_retweets(self):
        fake_retweets_links = json.load(open("data/fake_retweet_network.json"))
        for tweet_id, retweetd_id in tqdm(fake_retweets_links.items()):
            tweetid, origin_tweetdid = str(tweet_id), str(retweetd_id)

            # 新扩展进来的
            if tweetid not in self.url_tweets:
                d = find_tweet(tweetid)
                tweet = {
                    "tweet_id": str(d["tweet_id"]),
                    "user_id": str(d["user_id"]),
                    "dt": d["datetime_EST"],
                    "is_first": False,
                    "is_source": False,
                    "is_IRA": -1,
                    "URL": "[retweet]:" + origin_tweetdid,
                    "hostname": "[retweet]:" + origin_tweetdid
                }
                self.url_tweets[str(d["tweet_id"])] = tweet

            # 原来就有，而且原来推特就是fake news
            elif tweetid in self.url_tweets:
                self.url_tweets["tweetid"].update({
                        "is_first": False,
                        "is_source": False,
                        "URL": "[retweet]:" + origin_tweetdid,
                        "hostname": "[retweet]:" + origin_tweetdid
                })

            # else: # 我需要看你转发前是不是fake news，如果不是的话，我就不要了！
            #     # 这个情况很特殊，转发了别人的信息，然后附带了fake news URL，需要特别处理；这里不考虑
            #     del self.url_tweets[tweetid]

        # 什么是source？没有转发别人的！
        for url, values in self.url_tweets.items():
            if self.url_tweets[url]["is_source"] == -1:
                self.url_tweets[url]["is_source"] = True




