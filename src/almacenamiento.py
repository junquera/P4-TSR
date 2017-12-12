from pymongo import MongoClient
import datetime

import credentials

class Internal_DB():
    def __init__(self):
        # Client connection
        client = MongoClient('localhost', 27017)
        db = client.p4
        self.random_values = db.random_values

    def add_value(self, value):
        self.random_values.insert_one({
            'value': value,
            'date': datetime.datetime.utcnow()
        })

    def get_all(self):
        values =  self.random_values.find()
        return [value for value in values]

    def get_one(self):
        return self.random_values.find_one()


    def get_by_threshold(self, **kwargs):
        result = {}
        if 'max' in kwargs:
            result['max'] = self.random_values.find_one({
                'value': {'$gt':  kwargs['max']}
            })
        if 'min' in kwargs:
            result['min'] = self.random_values.find_one({
                'value': {'$lt': kwargs['min']}
            })
        return result
