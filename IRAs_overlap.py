#-*- coding: utf-8 -*-

"""
Created on 2018-11-16 09:01:28
@author: https://kayzhou.github.io/

12th week in NY
"""

from my_weapon import *
from SQLite_handler import get_user_id, find_tweet


class analyze_IRA_in_network:
    def __init__(self):
        self.author = "kay"
        self.user_id_map = {}

    def find_user_id_map(self):
        data = pd.read_csv("data/ira_tweets_csv_hashed.csv",
                            usecols=["tweetid", "userid"], dtype=str)
        with open("data/IRA_map_v3.json", "w") as f:
            for _, row in tqdm(data.iterrows()):
                tweet_id = row["tweetid"]
                user_id = row["userid"]
                # if user_id in self.user_id_map:
                #     continue
                d = find_tweet(tweet_id)
                if d:
                    # self.user_id_map[user_id] = real_user_id
                    f.write("{},{},{}\n".format(tweet_id, user_id, d["user_id"]))

    def check(self):
        # IRA_map_v2.json 较大库的映射
        map1 = []
        # SQLITE 数据库中的映射
        map2 = []


        # save
        # json.dump(self.user_id_map, open("data/IRA_map.json", "w"), indent=2)

    def run(self):
        self.find_user_id_map()

if __name__ == "__main__":
    Lebron = analyze_IRA_in_network()
    Lebron.run()
