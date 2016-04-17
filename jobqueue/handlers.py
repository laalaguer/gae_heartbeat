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
        GET /jobs?active=true,false
        - download json
    '''
    
    def get(self):
        active = self.request.get('active', None)
        jobs = None
        if  active == 'true':
            jobs = Job.query_whole_by_active(True) # an iterator.
        elif active == 'false':
            jobs = Job.query_whole_by_active(False) # an iterator.
        else:
            jobs = Job.query_whole()
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

# params: 
class UpdateJobStatusHandler(webapp2.RequestHandler):
    '''
    GET /updatejob/<item-id> : public_hash_id

    success - true
    response - a json object, about the job final result (You decide the content)

    success - false
    will_retry - true/false
    fail_reason - a string
    '''
    def post(self, hash_id):
        jsonstring = self.request.body
        payload = None
        try:
            payload = json.loads(jsonstring)
            if payload['success'] == True:
                if not payload['response']:
                    raise Exception('need response - a json object')
            elif payload['success'] == False:
                if not (payload['will_retry'] or payload['fail_reason']):
                    raise Exception('need will_retry, fail_reason')
            else:
                raise Exception('success parameter is either boolean true or false')
        except Exception as ex:
            self.error(400)
            self.response.out.write('Your Data Error, ' + str(ex))



        # step 1, get the job in the queue, but if not found, error 404
        try:
            jobs = Job.query_by_hash(str(hash_id)) # an iterator.
            if len(jobs):
                for each in jobs: # modify the job status according to the request
                    # step 2, stuff the job status with new data here.
                    if payload['success']:
                        each.success = True
                        each.will_retry = False
                        each.response = payload['response']
                    else:
                        each.success = False
                        each.will_retry = payload['will_retry']
                        each.fail_reason = payload['fail_reason']
                        each.fail_times = each.fail_times + 1 # add one to the failure times
                    each.put() # store it into database
                    self.response.out.write(each.public_hash_id)
            else:
                self.error(404)
                self.response.out.write('Job Not Found')
        except Exception as ex:
            self.error(500)
            self.response.out.write('Database Query Error ' + str(ex))

    def get(self, hash_id):
        self.post(hash_id)