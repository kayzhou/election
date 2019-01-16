import json

class Who_is_fake(object):
    def __init__(self):
        self.NEW_HOST_1 = {}
        for k, v in json.load(open("data/sources.json")).items():
            hostname = k.lower()
            _type = v["type"]
            if _type in ["fake", "conspiracy", "hate"]:
                self.NEW_HOST_1[hostname] = "FAKE"
            elif _type == "bias":
                self.NEW_HOST_1[hostname] = "BIAS"

        self.NEW_HOST_2 = {k.lower(): v for k, v in json.load(open("data/mbfc_host_label.json")).items()}

        self.HOST = {
                "thegatewaypundit.com": 0,
                "truthfeed.com": 0,
                "infowars.com": 0,
                "therealstrategy.com": 0,
                "conservativetribune.com": 0,
                "zerohedge.com": 0,
                "rickwells.us": 0,
                "departed.co": 0,
                "thepoliticalinsider.com": 0,
                "therightscoop.com": 0,
                "teaparty.org": 0,
                "usapoliticsnow.com": 0,
                "clashdaily.com": 0,
                "thefederalistpapers.org": 0,
                "redflagnews.com": 0,
                "thetruthdivision.com": 0,
                "breitbart.com": 1,
                "dailycaller.com": 1,
                "americanthinker.com": 1,
                "wnd.com": 1,
                "freebeacon.com": 1,
                "newsninja2012.com": 1,
                "hannity.com": 1,
                "newsmax.com": 1,
                "endingthefed.com": 1,
                "truepundit.com": 1,
                "westernjournalism.com": 1,
                "dailywire.com": 1,
                "newsbusters.org": 1,
                "ilovemyfreedom.org": 1,
                "100percentfedup.com": 1,
                "pjmedia.com": 1,
                "weaselzippers.us": 1,
                "foxnews.com": 2,
                "dailymail.co.uk": 2,
                "washingtonexaminer.com": 2,
                "nypost.com": 2,
                "bizpacreview.com": 2,
                "nationalreview.com": 2,
                "lifezette.com": 2,
                "redstate.com": 2,
                "allenbwest.com": 2,
                "theconservativetreehouse.com": 2,
                "townhall.com": 2,
                "investors.com": 2,
                "theblaze.com": 2,
                "theamericanmirror.com": 2,
                "ijr.com": 2,
                "judicialwatch.org": 2,
                "thefederalist.com": 2,
                "hotair.com": 2,
                "conservativereview.com": 2,
                "weeklystandard.com": 2,
                "wsj.com": 3,
                "washingtontimes.com": 3,
                "rt.com": 3,
                "realclearpolitics.com": 3,
                "telegraph.co.uk": 3,
                "forbes.com": 3,
                "fortune.com": 3,
                "cnn.com": 4,
                "thehill.com": 4,
                "politico.com": 4,
                "usatoday.com": 4,
                "reuters.com": 4,
                "bloomberg.com": 4,
                "businessinsider.com": 4,
                "apnews.com": 4,
                "observer.com": 4,
                "fivethirtyeight.com": 4,
                "bbc.com": 4,
                "ibtimes.com": 4,
                "bbc.co.uk": 4,
                "nytimes.com": 5,
                "washingtonpost.com": 5,
                "nbcnews.com": 5,
                "abcnews.go.com": 5,
                "theguardian.com": 5,
                "vox.com": 5,
                "slate.com": 5,
                "buzzfeed.com": 5,
                "cbsnews.com": 5,
                "politifact.com": 5,
                "latimes.com": 5,
                "nydailynews.com": 5,
                "theatlantic.com": 5,
                "mediaite.com": 5,
                "newsweek.com": 5,
                "npr.org": 5,
                "independent.co.uk": 5,
                "cnb.cx": 5,
                "hollywoodreporter.com": 5,
                "huffingtonpost.com": 6,
                "thedailybeast.com": 6,
                "dailykos.com": 6,
                "rawstory.com": 6,
                "politicususa.com": 6,
                "time.com": 6,
                "motherjones.com": 6,
                "talkingpointsmemo.com": 6,
                "msnbc.com": 6,
                "mashable.com": 6,
                "salon.com": 6,
                "thinkprogress.org": 6,
                "newyorker.com": 6,
                "mediamatters.org": 6,
                "nymag.com": 6,
                "theintercept.com": 6,
                "thenation.com": 6,
                "people.com": 6,
                "dailynewsbin.com": 7,
                "bipartisanreport.com": 7,
                "bluenationreview.com": 7,
                "crooksandliars.com": 7,
                "occupydemocrats.com": 7,
                "shareblue.com": 7,
                "usuncut.com": 7
            }



    def identify(self, ht):
        ht = ht.lower()
        # labels = []
        # if ht in self.NEW_HOST_1:
        #     labels.append(self.NEW_HOST_1[ht])
        # else:
        #     labels.append("GOOD")
        # if ht in self.NEW_HOST_2:
        #     labels.extend(self.NEW_HOST_2[ht])
        # else:
        #     labels.extend([-1, -1])
        if ht in self.HOST:
            return self.HOST[ht]
        else:
            return -1

    def is_fake(self, ht):
        if self.identify(ht)[0] == "FAKE":
            return True
        else:
            return False

class Are_you_IRA(object):
    def __init__(self):
        self._map = json.load(open("data/IRA_map.json"))
        self.IRA_users_before_set = set(self._map.keys())
        self.IRA_user_set = set(self._map.values())

    def fuck(self, ht):
        return ht in self.IRA_user_set


if __name__ == "__main__":
    who = Who_is_fake()
    print(who.identify("baidu.com"))




