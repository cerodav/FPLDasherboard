class LiveFPLAverageDataStore:

    def __init__(self):
        self.top10KAvg = None
        self.top10KHitsAvg = None
        self.top10KHitsInclAvg = None
        self.overallAvg = None
        self.overallHitsAvg = None
        self.overallHitsInclAvg = None
        self.gw = None

    def isEmpty(self):
        if not all([self.top10KAvg, self.top10KHitsAvg, self.top10KHitsInclAvg, self.overallAvg, self.overallHitsAvg, self.overallHitsInclAvg]):
            return True
        return False

    def getTop10KAvg(self):
        return self.top10KAvg

    def getTop10KHitsAvg(self):
        return self.top10KHitsAvg

    def getTop10KHitsInclAvg(self):
        return self.top10KHitsInclAvg

    def getOverallAvg(self):
        return self.overallAvg

    def getOverallHitsAvg(self):
        return self.overallHitsAvg

    def getOverallHitsInclAvg(self):
        return self.overallHitsInclAvg

    def getGameweek(self):
        return self.gw





