import os
import pickle
from pathlib import Path
from fpldb.utils.configFileUtil import ConfigFileUtil

class PickleUtil():

    pickleDirPath = Path(ConfigFileUtil().getConfig('picklePath'))

    @staticmethod
    def saveToPickle(data, fileName, path=None):
        if path is None:
            path = PickleUtil.pickleDirPath
        completeFilePath = os.path.join(path, '{}.pkl'.format(fileName))
        fHandler = open(completeFilePath, 'wb')
        pickle.dump(data, fHandler)
        fHandler.close()

    @staticmethod
    def getDataFromPickle(fileName, path=None):
        if path is None:
            path = PickleUtil.pickleDirPath
        completeFilePath = os.path.join(path, '{}.pkl'.format(fileName))
        if not os.path.isfile(completeFilePath):
            return None
        fHandler = open(completeFilePath, 'rb')
        data = pickle.load(fHandler)
        fHandler.close()
        return data