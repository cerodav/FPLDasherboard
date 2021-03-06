import json
from enum import Enum
from tornado.web import RequestHandler
from fpldb.api.officialFPL.officialFPLApi import OfficialFPLApi

class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.name
        return json.JSONEncoder.default(self, obj)

class BaseHandler(RequestHandler):
    """Only allow GET requests."""
    SUPPORTED_METHODS = ["GET"]

    fplApi = OfficialFPLApi()
    staticDataBootstrap = fplApi.getStaticDataBootstrap()
    staticPlayerData = fplApi.getStaticPlayerData()
    staticTeamData = fplApi.getStaticTeamData()

    def get(self):
        pass

    def setPathInfo(self):
        path = self.request.path
        splits = path.split('/')
        self.pathInfo = {x-2:splits[x] for x in range(2, len(splits))}

    def set_default_headers(self):
        """Set the default response header to be JSON."""
        self.set_header("Content-Type", 'application/json; charset="utf-8"')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def send_response(self, data, status=200):
        """Construct and send a JSON response with appropriate status code."""
        self.set_status(status)
        jsonData = json.dumps(data, cls=CustomJsonEncoder).replace("</", "<\\/")
        self.write(jsonData)

    def prepare(self):
        self.setPathInfo()