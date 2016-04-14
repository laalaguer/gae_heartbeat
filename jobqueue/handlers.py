import webapp2
from db import Job
import db
import json


class SingleJobJsonHandler(webapp2.RequestHandler):
    ''' Read a certain object with hash value, not urlsafekey
        GET /jobs/<item-id>
        - download json
    '''
    
    def get(self, hash_id):
        jobs = Job.query_by_hash(str(hash_id)) # an iterator.
        json_dict = {}
        json_dict['jobs'] = []
        for job in jobs:
            json_dict['jobs'].append(job.to_dict(exclude=['add_date'])) # we don't want to include date objects.
        
        self.response.charset = 'utf-8'
        self.response.content_type = 'application/json'
        self.response.out.write(json.dumps(json_dict,ensure_ascii=False,indent=2, sort_keys=True).encode('utf-8'))

class AllJobJsonHandler(webapp2.RequestHandler):
    ''' Read all jobs inside the database
        GET /jobs
        - download json
    '''
    
    def get(self):
        jobs = Job.query_whole() # an iterator.
        json_dict = {}
        json_dict['jobs'] = []
        for job in jobs:
            json_dict['jobs'].append(job.to_dict(exclude=['add_date'])) # we don't want to include date objects.
        
        self.response.charset = 'utf-8'
        self.response.content_type = 'application/json'
        self.response.out.write(json.dumps(json_dict,ensure_ascii=False,indent=2, sort_keys=True).encode('utf-8'))


# parameters: 
class CreateJobHandler(webapp2.RequestHandler):
    def get(self):
        try:
            jsonstring = self.request.body
            payload = json.loads(jsonstring)
            if payload:
                key_value = db.put_job(payload)
                self.response.out.write(key_value)
            else:
                self.error(400)
                self.response.out.write('Payload Empty')
        except Exception as ex:
            self.error(400)
            self.response.out.write(type(ex).__name__ + str(ex))

    def post(self):
        self.get() # redirect to get()

# parameters: name
class DeleteJobHandler(webapp2.RequestHandler):
    ''' delete all the matching job, by hash'''
    def get(self, hash_id):
        try:
            self.response.out.write(db.delete_job(str(hash_id)))
        except:
            self.error(500)