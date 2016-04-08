import webapp2
import os
import jinja2
import heartbeat.handlers

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

config = {}

app = webapp2.WSGIApplication(routes=[
    ('/heartbeat/list', heartbeat.handlers.FetchHeartBeatJsonHandler),
    ('/heartbeat/create', heartbeat.handlers.CreateHeartBeatHandler),
    ('/heartbeat/delete', heartbeat.handlers.DeleteHeartBeatHandler)
], debug=True, config=config)