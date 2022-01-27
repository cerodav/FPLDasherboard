import requests
import os
from fpldb.api.officialFPL.officialFPLApi import OfficialFPLApi

def downloadAllTeamLogos():
    teamData = OfficialFPLApi.getStaticTeamData()
    teamCodes = [x['code'] for x in teamData.values()]
    teamId = [x['id'] for x in teamData.values()]
    dirPath= r'D:\Sherine Davis\Code\PycharmProjects\FPLDasherboard\fpldb\resources\img\teamLogo'
    for id, code in zip(teamId, teamCodes):
        data = requests.get('https://fantasy.premierleague.com/dist/img/badges/badge_{}_40.png'.format(code))
        fileName = 'badge_{}_40.png'.format(id)
        f = open(os.path.join(dirPath, fileName), 'wb')
        f.write(data.content)
        f.close()

def downloadAllTeamJersey():
    teamData = OfficialFPLApi.getStaticTeamData()
    teamCodes = [x['code'] for x in teamData.values()]
    teamId = [x['id'] for x in teamData.values()]
    dirPath= r'D:\Sherine Davis\Code\PycharmProjects\FPLDasherboard\fpldb\resources\img\teamJersey'
    for id, code in zip(teamId, teamCodes):
        data = requests.get('https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_{}-66.png'.format(code))
        fileName = 'shirt_{}_66.png'.format(id)
        f = open(os.path.join(dirPath, fileName), 'wb')
        f.write(data.content)
        f.close()

if __name__ == '__main__':
    downloadAllTeamLogos()