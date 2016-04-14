from google.appengine.ext import ndb
import hashlib
import datetime
import random

class Job(ndb.Model):
    public_hash_id = ndb.StringProperty(default='') # a random job id, for marking purpose.
    add_date = ndb.DateTimeProperty(auto_now_add=True)
    add_date_str = ndb.StringProperty(default='') # string represent of adding date

    payload = ndb.JsonProperty() # job payloads of job requirement. inside can be flexible.

    success = ndb.BooleanProperty(default=False) # if job is done or not.
    will_retry = ndb.BooleanProperty(default=True) # if job will be retry if failed.
    fail_reason = ndb.StringProperty(default='') # why the job execution failed.
    
    response = ndb.JsonProperty() # job execution result : justificante, fecha, hora as dict key. inside can be flexible.

    # Generate a public hash, we don't want to use the urlsafe hash from GAE
    def _pre_put_hook(self):
        m = hashlib.md5()
        factor_one = datetime.datetime.utcnow().strftime('%Y/%m/%d %H:%M:%S')
        factor_two = str(random.getrandbits(128))
        m.update(factor_one)
        m.update(factor_two)
        self.public_hash_id = m.hexdigest()

        self.add_date_str = factor_one

    @classmethod
    def query_by_hash(cls, hash_value):
        return cls.query(cls.public_hash_id == hash_value).order(-cls.add_date).fetch()

    @classmethod
    def query_whole(cls):
        return cls.query().order(-cls.add_date).fetch()

def put_job(payload):
    response = {
        'justificante' : '',
        'fecha' : '',
        'hora' : '',
    }

    job = Job(payload=payload, response=response)
    job.put() # store in db
    return job.public_hash_id # return the public hash id


def delete_job(hash_id):
    ''' delete all hash_id related items'''
    existing = Job.query_by_hash(hash_id)
    length = len(existing)
    for each in existing:
        each.key.delete() # delete matching entries.

    return length # return the deleted entries numbers