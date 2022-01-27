from collections import defaultdict
from datetime import datetime

import pandas as pd

from threading import Thread
from fpldb.utils.coreUtils import CoreUtils
from fpldb.dashboardService.handlers.baseHandler import BaseHandler
from fpldb.logger.logger import logger
from fpldb.dashboardService.dataCollectors.telegramChannelMessageDataStore import TelegramChannelMessageDataStore
from fpldb.dashboardService.dataCollectors.telegramChannelMessageCollector import TelegramChannelMessageCollector

class NewsUpdatesHandler(BaseHandler):
    telegramUpdates = TelegramChannelMessageDataStore()
    Thread(target=TelegramChannelMessageCollector.run, args=(telegramUpdates, CoreUtils.getGameweek())).start()

    async def get(self):
        logger.info('[INCOMING] Request at /news-updates/.* {} '.format(self.request.path))
        parentPath = self.pathInfo[1].upper()
        try:
            if parentPath == 'NEWS':
                response = self.getLatestNews()
            elif parentPath == 'LIVE-UPDATES':
                response = self.getLatestUpdates()
            self.send_response(response)
            logger.info('[OUTGOING] Response for /news-updates/.* {} '.format(self.request.path))
        except Exception as e:
            logger.exception('[EXCEPTION] While trying to respond to query {}'.format(self.request.path))

    def getLatestNews(self):
        news = NewsUpdatesHandler.telegramUpdates.getNews()
        return news

    def getLatestUpdates(self):
        upd = NewsUpdatesHandler.telegramUpdates.getUpdates()
        return upd
