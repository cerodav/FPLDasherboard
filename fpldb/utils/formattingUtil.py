from datetime import datetime

class FormattingUtil:

    @staticmethod
    def getDatetimeFromDatetimeString(input, inputFormat='%Y-%m-%dT%H:%M:%S.%fZ'):
        d = datetime.strptime(input, inputFormat)
        return d
