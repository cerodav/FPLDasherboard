import os
import yaml
import pathlib

class ConfigFileUtil:

    config = None
    configFilePath = None
    isSetup = False

    def __init__(self, config = None, configFilePath = None):
        self.config = config
        self.configFilePath = configFilePath
        self.setup()

    def setup(self):
        if self.config is None:
            if self.configFilePath is None:
                self.configFilePath = self.getConfigFilePath()
            self.loadConfig()

    def getCurrentScriptDirectory(self):
        return pathlib.Path(__file__).parent.absolute()

    def getConfigFilePath(self):
        configFilePath = os.getenv('FPLDB_CONFIG_PATH', None)
        if configFilePath is None:
            curentScriptDir = self.getCurrentScriptDirectory()
            fpldbPath = curentScriptDir.parent.absolute()
            configFilePath = os.path.join(fpldbPath, 'other', 'config.yaml')
        return configFilePath

    def loadConfig(self):
        file = open(self.configFilePath)
        self.config = yaml.full_load(file)

    def getConfig(self, name, default = None):
        return self.config.get(name, default)

if __name__ == '__main__':
    c = ConfigFileUtil()
    print(c.getConfig('logFilePath'))
