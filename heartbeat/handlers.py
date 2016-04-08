# Webapp2 handlers of the database
# You can use it anywhere if you like in your project.
import webapp2
import json
import db # our database in the module

# parameters: name,
class FetchHeartBeatJsonHandler(webapp2.RequestHandler):
    ''' return matching heartbeat as a json string '''
    def get(self):
        # name of the the heartbeat
        name = self.request.get('name', None)
        # try to response json
        self.response.headers['Content-Type'] = 'application/json'
        existing = db.get_heartbeats(name)

        return_dict = {}
        return_dict['heartbeats'] = [] # heartbeats list

        if len(existing)>0:
            for each in existing:
                return_dict['heartbeats'].append(each.to_dict(exclude=['datetime'])) # we dont need the insert time of object
        
        self.response.out.write(json.dumps(return_dict,indent=2))

# parameters: name, is_on, come_back,  each_round_if_success, each_round_if_fail
class CreateHeartBeatHandler(webapp2.RequestHandler):
    def get(self):
        try:
            name = self.request.get('name', 'default') # if not named, create a default heartbeat
            is_on = int(self.request.get("is_on", '0'))
            come_back = int(self.request.get("come_back", '5'))
            each_round_if_success = int(self.request.get("each_round_if_success", '5'))
            each_round_if_fail = int(self.request.get("each_round_if_fail", '5'))

            key_value = db.put_heartbeat(name=name,
                                        is_on=is_on,
                                        come_back=come_back,
                                        each_round_if_success=each_round_if_success,
                                        each_round_if_fail=each_round_if_fail)

            self.response.out.write(key_value)
        except:
            self.response.out.write('ERROR')

    def post(self):
        self.get() # redirect to get()

# parameters: name
class DeleteHeartBeatHandler(webapp2.RequestHandler):
    ''' delete all the matching heartbeat, by name'''
    def get(self):
        # name of the the heartbeat
        name = self.request.get('name', None)
        try:
            self.response.out.write(db.delete_heartbeats(name))
        except:
            self.response.out.write('ERROR')