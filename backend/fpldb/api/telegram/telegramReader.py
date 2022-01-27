import configparser
import json
from telethon import TelegramClient
from fpldb.utils.configFileUtil import ConfigFileUtil
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel
import asyncio


class TelegramReader:

    def __init__(self):
        self.connConfigs = {}
        self.client = None
        self.connEstablished = False
        self.channel = None
        self.channelURL = None

    def getConnectionConfigs(self):
        configs = ConfigFileUtil().getConfig('telegram', default=None)
        apiId = configs['api_id']
        apiHash = configs['api_hash']
        apiHash = str(apiHash)
        username = configs['username']
        self.channelURL = configs['channel']
        self.connConfigs = {
            'apiId': apiId,
            'apiHash': apiHash,
            'userName': username,
        }

    async def getConnection(self):
        self.client = TelegramClient(self.connConfigs.get('userName'),
                                self.connConfigs.get('apiId'),
                                self.connConfigs.get('apiHash'))
        await self.client.start()
        if not await self.client.is_user_authorized():
            raise Exception('[TELEGRAM] Auth failed')
        await self.setChannel()

    async def getMessagesFromChannel(self, limit=100):
        await self.getConnection()
        allMessages = []
        taken = 0
        offsetId = 0
        while taken < limit:
            toPull = 100 if limit - taken > 100 else limit - taken
            history = await self.client(GetHistoryRequest(
                peer=self.channel,
                offset_id=offsetId,
                offset_date=None,
                add_offset=0,
                limit=toPull,
                max_id=0,
                min_id=0,
                hash=0
            ))
            messages = history.messages
            for message in messages:
                allMessages.append(message.to_dict())
            offsetId = messages[-1].id
            taken += toPull
        return allMessages

    async def setChannel(self):
        myChannel = await self.client.get_entity(self.channelURL)
        self.channel = myChannel

if __name__ == '__main__':
    t = TelegramReader()
    t.getConnectionConfigs()
    m = asyncio.run(t.getMessagesFromChannel(limit=15))
    print('Process completed')





