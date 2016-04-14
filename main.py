import webapp2
import os
import jinja2
import heartbeat.handlers
import jobqueue.handlers

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

config = {}

app = webapp2.WSGIApplication(routes=[
    ('/heartbeat/list', heartbeat.handlers.FetchHeartBeatJsonHandler),
    ('/heartbeat/create', heartbeat.handlers.CreateHeartBeatHandler),
    ('/heartbeat/delete', heartbeat.handlers.DeleteHeartBeatHandler),

    ('/job/create', jobqueue.handlers.CreateJobHandler),
    webapp2.Route('/job/list', handler=jobqueue.handlers.AllJobJsonHandler),
    webapp2.Route('/job/list/<hash_id>', handler=jobqueue.handlers.SingleJobJsonHandler),
    webapp2.Route('/job/delete/<hash_id>', handler=jobqueue.handlers.DeleteJobHandler),
], debug=True, config=config)