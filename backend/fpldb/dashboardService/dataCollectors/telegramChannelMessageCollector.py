import time
import asyncio
import pandas as pd
from datetime import datetime, timedelta
from fpldb.api.telegram.telegramReader import TelegramReader
from fpldb.api.officialFPL.officialFPLApi import OfficialFPLApi
from fpldb.dashboardService.dataCollectors.telegramChannelMessageDataStore import TelegramChannelMessageDataStore

class TelegramChannelMessageCollector():

    gw = None
    sleepTime = None
    liveDatastore = None
    sleepTimeWhileActive = None
    reader = None

    @staticmethod
    def isMatchPlaying(offset = 300, retryEnabled = True, retrySleepTime = 5, retryCount = 5):
        while True and retryEnabled and retryCount > 0:
            try:
                fixtureList = OfficialFPLApi.getFixtures(TelegramChannelMessageCollector.gw)
                fixtureTimes = [(pd.to_datetime(x['kickoff_time']), pd.to_datetime(x['kickoff_time']) + timedelta(minutes = 115))  for x in fixtureList]
                for fixtureTime in fixtureTimes:
                    if fixtureTime[0] <= datetime.now(fixtureTime[0].tzinfo) and datetime.now(fixtureTime[1].tzinfo) <= fixtureTime[1]:
                        return True
                return False
            except Exception as e:
                time.sleep(retrySleepTime)
                retryCount -= 1
        raise Exception('No data returned from API')

    @staticmethod
    def run(datastore, gw, sleepTime=10800, sleepTimeWhileActive=120):

        TelegramChannelMessageCollector.reader = TelegramReader()
        TelegramChannelMessageCollector.liveDatastore = datastore
        TelegramChannelMessageCollector.gw = gw
        TelegramChannelMessageCollector.sleepTime = sleepTime
        TelegramChannelMessageCollector.sleepTimeWhileActive = sleepTimeWhileActive
        TelegramChannelMessageCollector.reader.getConnectionConfigs()

        while True:
            isActive = TelegramChannelMessageCollector.isMatchPlaying()
            if TelegramChannelMessageCollector.isStoreEmpty() or isActive:
                messages = asyncio.run(TelegramChannelMessageCollector.reader.getMessagesFromChannel(limit=200))
                news, updates = TelegramChannelMessageCollector.parseMessages(messages)
                TelegramChannelMessageCollector.saveData(news, updates)
            if isActive:
                time.sleep(TelegramChannelMessageCollector.sleepTimeWhileActive)
            else:
                time.sleep(TelegramChannelMessageCollector.sleepTime)

    @staticmethod
    def parseMessages(messages):
        news = []
        updates = []
        speakingChr = chr(128483)
        alarmChr = chr(128680)
        ambulanceChr = chr(127973)
        weirdChr = chr(65039)
        for idx, message in enumerate(messages):
            if 'Price Rises' in message['message'] \
                    or 'Price Falls' in message['message'] \
                    or 'Statistics!' in message['message'] \
                    or 'SCOUT SELECTION' in message['message'] \
                    or alarmChr in message['message']:
                continue
            if 'FULL TIME' in message['message']:
                t = 'FT'
                partA, partB = message['message'].split('\n')[-1].split('-')
                aS, a = partB[0], partB[1:-1]
                hS, h = partA[-1], partA[1:-1]
                msg = {
                    'type': t,
                    'goal': None,
                    'assist': None,
                    'home': h,
                    'away': a,
                    'redCard': None,
                    'homeScore': hS,
                    'awayScore': aS,
                    'content': message['message'],
                    'timestamp': message['date'].isoformat()
                }
                updates.append(msg)
                continue
            if 'BREAKING NEWS' in message['message']:
                newsObj = {}
                newsTitle = 'BREAKING NEWS'
                tempNews = [x for x in message['message'].split('\n')[1:] if x != '' and not x.startswith('#FPL')]
                newsObj['title'] = newsTitle
                newsObj['content'] = tempNews
                newsObj['timestamp'] = message['date'].isoformat()
                news.append(newsObj)
                continue
            if message['message'].startswith('Lineups'):
                newsObj = {}
                newsTitle = message['message'].split('\n')[0].rstrip()
                tempNews = [x for x in message['message'].split('\n')[1:] if x != '']
                newsObj['title'] = newsTitle
                newsObj['content'] = tempNews
                newsObj['timestamp'] = message['date'].isoformat()
                news.append(newsObj)
                continue
            if 'TEAM NEWS' in message['message']:
                newsObj = {}
                sIdx = idx - 1
                charType = speakingChr if speakingChr in message['message'] else ambulanceChr
                newsTitle = message['message'].split(charType)[0].rstrip()
                tempNews = message['message'].split(charType)[1:]
                while sIdx >= 0 and 'TEAM NEWS' not in messages[sIdx]['message'] and charType in messages[sIdx]['message']:
                    tempNews.extend(messages[sIdx]['message'].split(charType)[1:])
                    sIdx -= 1
                newsObj['title'] = newsTitle
                newsObj['content'] = [x.replace(weirdChr, ' ').lstrip() for x in tempNews]
                newsObj['timestamp'] = message['date'].isoformat()
                news.append(newsObj)
                continue
            g = None
            a = None
            r = None
            if '#FPL' in message['message']:
                if 'goal' not in message['message'].lower() \
                        and 'red card' not in message['message'].lower():
                    continue
                t = 'EVENT'
                if 'goal' in message['message'].lower():
                    if 'own goal' in message['message'].lower():
                        t = 'OWN_GOAL'
                    else:
                        t = 'GOAL'
                    for strg in message['message'].split('\n'):
                        if 'goal - ' in strg.lower():
                            g = strg.split()[-1]
                        if 'assist - ' in strg.lower():
                            a = strg.split()[-1]
                elif 'red card' in message['message'].lower():
                    t = 'RED_CARD'
                    for strg in message['message'].split('\n'):
                        if 'red card - ' in strg.lower():
                            r = strg.split()[-1]
                msg = {
                    'type': t,
                    'goal': g,
                    'assist': a,
                    'redCard': r,
                    'home': None,
                    'away': None,
                    'homeScore': None,
                    'awayScore': None,
                    'content': message['message'],
                    'timestamp': message['date'].isoformat()
                }
                updates.append(msg)
                continue
        return news, updates

    @staticmethod
    def isStoreEmpty():
        return TelegramChannelMessageCollector.liveDatastore.isEmpty()

    @staticmethod
    def saveData(news, updates):
        TelegramChannelMessageCollector.liveDatastore.setNews(news)
        TelegramChannelMessageCollector.liveDatastore.setUpdates(updates)

if __name__ == '__main__':
    t = TelegramChannelMessageDataStore()
    TelegramChannelMessageCollector.run(t, 19)