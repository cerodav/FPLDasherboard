class TelegramChannelMessageDataStore:

    def __init__(self):
        self.news = []
        self.updates = []
        self.lastUpdateTimestamp = None

    def isEmpty(self):
        return len(self.news) == 0 or len(self.updates) == 0

    def getNews(self):
        return self.news

    def getUpdates(self):
        return self.updates

    def setNews(self, news):
        self.news = news

    def setUpdates(self, updates):
        self.updates = updates





