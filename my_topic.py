#-*- coding: utf-8 -*-

"""
Created on 2019-01-27 17:55:17
@author: https://kayzhou.github.io/
"""

import sqlite3

from gensim.models import LdaModel
from gensim.corpora import Dictionary
from tqdm import tqdm

from Trump_Clinton_Classifer.TwProcess import CustomTweetTokenizer

tokenizer = CustomTweetTokenizer(preserve_case=False,
                                 reduce_len=True,
                                 strip_handles=False,
                                 normalize_usernames=False,
                                 normalize_urls=True,
                                 keep_allupper=False)

conn = sqlite3.connect(
    "/home/alex/network_workdir/elections/databases_ssd/complete_trump_vs_hillary_db.sqlite")
c = conn.cursor()
c.execute('''SELECT text FROM tweet LIMIT 100''')
texts = [tokenizer.tokenize(d[0]) for d in c.fetchall()]
dictionary = Dictionary(texts)

corpus = [dictionary.doc2bow(t) for t in texts]
lda = LdaModel(corpus, num_topics=10)
conn.close()

# conn = sqlite3.connect(
#     "/home/alex/network_workdir/elections/databases_ssd/complete_trump_vs_hillary_sep-nov_db.sqlite")

