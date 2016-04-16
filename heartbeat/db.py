from google.appengine.ext import ndb

class HeartBeat(ndb.Model):
    name = ndb.StringProperty(default='default') # name of the heart beat
    is_on = ndb.IntegerProperty(default=False) # if the worker should be on or not
    come_back = ndb.IntegerProperty(default=5) # default rate for calling this api, in minute.
    each_round_if_success = ndb.IntegerProperty(default=5) # default inter-mission between each crawler round.
    each_round_if_fail = ndb.IntegerProperty(default=5) # default inter-mission between each crawler round.
    datetime = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def query_whole(cls):
        ''' fetch the all of data '''
        return cls.query().order(-cls.datetime).fetch()

    @classmethod
    def query_last(cls, number):
        ''' fetch the latest numbers of data'''
        return cls.query().order(-cls.datetime).fetch(number)

    @classmethod
    def query_by_name(cls, name):
        ''' fetch the latest numbers of data'''
        return cls.query(cls.name == name).order(-cls.datetime).fetch() # fetch all with the name

def put_heartbeat(name, is_on, come_back, each_round_if_success, each_round_if_fail):
    ''' Insert a heartbeat into database.
        if name exists, then delete old ones, insert a new one.
        if name doesn't exists, then insert a new one.
    '''
    existing = HeartBeat.query_by_name(name)
    if len(existing) > 0:
        for each in existing:
            each.key.delete() # delete old

    item = HeartBeat(name=name,is_on=is_on, come_back=come_back, each_round_if_fail=each_round_if_fail, each_round_if_success=each_round_if_success)
    return item.put() # return the key value if put is success

def get_heartbeats(name=None):
    ''' return all the heartbeats with specifice name in the database
        if name is None, then get all heartbeats regardless of the name
    '''
    if name:
        return HeartBeat.query_by_name(name)
    else:
        return HeartBeat.query_whole()

def delete_heartbeats(name=None):
    ''' delete all heartbeats with the name, if name is None, delete all heartbeats regardless of the name'''
    existing = []
    if name:
        existing = HeartBeat.query_by_name(name)
    else:
        existing = HeartBeat.query_whole()
    if len(existing) > 0:
        for each in existing:
            each.key.delete() # delete matching entries.

    return len(existing) # return the deleted entries