from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application
from fpldb.logger.logger import logger
from fpldb.dashboardService.handlers.classicLeagueLiveHandler import ClassicLeagueLiveHandler

define('port', default=8086, help='Port to listen on')

"""Construct and serve the tornado application."""

app = Application([
    ('/api/live/.*', ClassicLeagueLiveHandler),
    ('/admin-api/.*', ClassicLeagueLiveHandler)
])

http_server = HTTPServer(app)
http_server.listen(options.port)
logger.info('Dashboard service listening on http://localhost:%i' % options.port)
IOLoop.current().start()
