import os
import json
from threading import Thread, Timer

class DBKeyValueError(Exception):
    pass
class DBFileError(Exception):
    pass

class yDB:

    key_is_not_string = DBKeyValueError('Key must be a string!')
    value_is_not_json = DBKeyValueError('Value must be a JSON object!')
    key_alredy_exist = DBKeyValueError('Key already exist!')
    key_not_present = DBKeyValueError('Key not exist!')
    file_size_greater_than_1gb = DBFileError("Database size exceeds 1GB")

    def __init__(self,name, location='/home/yogesh/Desktop/'):
        '''Creates database object and load data from location'''
        location += name
        self.load(location)
        self.dthread = None

    def load(self, location):
        '''Loads, reloads or changes the path to the db file'''
        location = os.path.expanduser(location)
        self.loco = location
        if os.path.exists(location):  #file already exist then load data
            try: 
                self.db = json.load(open(self.loco, 'rt'))
            except ValueError:
                if os.stat(self.loco).st_size == 0:  #file is empty
                    self.db = {}
                else:
                    raise  #avoid overwriting it
        else:
            self.db = {}
            self._dump()
        return True

    def _dump(self):
        '''Store into file'''
        json.dump(self.db, open(self.loco, 'wt'))
        if os.path.getsize(self.loco) > 1073741824:
            raise self.file_size_greater_than_1gb
        self.dthread = Thread(
            target=json.dump,
            args=(self.db, open(self.loco, 'wt')))
        self.dthread.start()
        self.dthread.join()

    def create(self, key, value,time_to_live_property=None):
        '''Set the str value of a key to JSON value'''
        if key in self.db:
            raise self.key_alredy_exist
        elif isinstance(key, str):
            if isinstance(value, dict):
                self.db[key] = value
                self._dump()
                if time_to_live_property!=None:
                    start_time = Timer(time_to_live_property,self.delAfterTime,[key])
                    start_time.start()
                return True
            else:
                raise self.value_is_not_json
        else:
            raise self.key_is_not_string

    def read(self, key):
        '''Get the value of a key'''
        if key in self.db:
            return self.db[key]
        else:
            raise self.key_not_present

    def delete(self, key):
        '''Delete a key'''
        if key in self.db:
            del self.db[key]
            self._dump()
            return True
        else:
            raise self.key_not_present

    def delAfterTime(self,key):
        self.delete(key)
