# Webapp2 handlers
# Handler is for human beings to operate.
# You can think of it as : human operation interface
import webapp2
import json
import jinja2


class DisplayAdminConsole(webapp2.RequestHandler):
    def get(self):
        jobqueue_db = self.app.config['jobqueue.db']
        jobs_active = jobqueue_db.Job.query_whole_by_active(True)
        for each in jobs_active:
            each.payload_raw_code = json.dumps(each.to_dict(include=['payload'],exclude=['add_date']),indent=2)

        jobs_dead = jobqueue_db.Job.query_whole_by_active(False)
        for each in jobs_dead:
            each.payload_raw_code = json.dumps(each.to_dict(include=['payload'],exclude=['add_date']),indent=2)
            each.response_raw_code = json.dumps(each.to_dict(include=['response'],exclude=['add_date']),indent=2)
        
        heartbeat_db = self.app.config['heartbeat.db']
        heartbeats_all = heartbeat_db.HeartBeat.query_whole()
        for each in heartbeats_all:
            each.raw_code = json.dumps(each.to_dict(exclude=['datetime']),indent=2)
        
        d = dict()
        d['jobs_active'] = jobs_active
        d['jobs_dead'] = jobs_dead
        d['heartbeats_all'] = heartbeats_all
        
        jinja_environment = self.app.config['jinja2_env']
        template = jinja_environment.get_template('/html/display-admin-console.html')
        self.response.out.write(template.render(d))

class AddAdminConsole(webapp2.RequestHandler):
    def get(self):
        jinja_environment = self.app.config['jinja2_env']
        template = jinja_environment.get_template('/html/add-admin-console.html')
        self.response.out.write(template.render(dict()))
        
class EchoHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("GET")
        self.response.out.write("<br>")
        self.response.out.write(self.request.GET)
        
    def post(self):
        self.response.out.write("POST")
        self.response.out.write("<br>")
        self.response.out.write(self.request.body)