from enum import Enum

class ActivityStatus(Enum):
    Completed = 1
    Failed = 2
    Processing = 3
    Started = 4
    Skipped = 5

class PlayerPosition(Enum):
    Attacker = 4
    Midfielder = 3
    Defender = 2
    Goalkeeper = 1

    @staticmethod
    def getPlayerPosition(id):
        if id is None:
            return None
        playerPositionMap = {x.value:x for x in PlayerPosition}
        if id in playerPositionMap:
            return playerPositionMap[id]
        else:
            return None

if __name__ == '__main__':
    PlayerPosition.getPlayerPosition(1)