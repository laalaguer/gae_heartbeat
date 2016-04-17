import webapp2
import os
import jinja2
import heartbeat.handlers
import jobqueue.handlers
import human.handlers
import jobqueue.db
import heartbeat.db

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

# this config is shared accross all the application, so use wisely.
config = {}
config['jinja2_env'] = jinja_environment
config['jobqueue.db'] = jobqueue.db
config['heartbeat.db'] = heartbeat.db

app = webapp2.WSGIApplication(routes=[
    ('/heartbeat/list', heartbeat.handlers.FetchHeartBeatJsonHandler),
    ('/heartbeat/create', heartbeat.handlers.CreateHeartBeatHandler),
    ('/heartbeat/delete', heartbeat.handlers.DeleteHeartBeatHandler),

    ('/job/create', jobqueue.handlers.CreateJobHandler),
    webapp2.Route('/job/list', handler=jobqueue.handlers.AllJobJsonHandler),
    webapp2.Route('/job/list/<hash_id>', handler=jobqueue.handlers.SingleJobJsonHandler),
    webapp2.Route('/job/delete/<hash_id>', handler=jobqueue.handlers.DeleteJobHandler),
    webapp2.Route('/job/update/<hash_id>', handler=jobqueue.handlers.UpdateJobStatusHandler),
        
    ('/admin-display', human.handlers.DisplayAdminConsole),
    ('/admin-add', human.handlers.AddAdminConsole),
    ('/echo', human.handlers.EchoHandler),
], debug=True, config=config)