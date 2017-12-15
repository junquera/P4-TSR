from pymongo import MongoClient
from app.xively import Xively
import datetime

class Internal_DB():
    def __init__(self):
        # Client connection
        client = MongoClient('localhost', 27017)
        print("Mongo connection stablished!")
        db = client.p4
        self.random_values = db.random_values
        self.random_values.delete_many({})

    def add_value(self, value, time=None):
        if time is None:
            time = datetime.datetime.utcnow().replace(microsecond=0).isoformat()
        self.random_values.insert_one({
            'value': value,
            'date': time
        })

    def get_all(self):
        values =  self.random_values.find()
        return [value for value in values]

    def get_one(self):
        return self.random_values.find_one()


    def get_by_threshold(self, **kwargs):
        result = {}
        if 'min' in kwargs:
            if not kwargs['min'] is None:
                try:
                    min = float(kwargs['min'])
                    min_vs = self.random_values.find({
                        'value': {'$lt':  min}
                    })
                    result['min'] = [value for value in min_vs]
                except:
                    pass
        if 'max' in kwargs:
            if not kwargs['max'] is None:
                try:
                    max = float(kwargs['max'])
                    max_vs = self.random_values.find({
                        'value': {'$gt': max}
                    })
                    result['max'] = [value for value in max_vs]
                except:
                    pass
        return result


class External_DB():
    def __init__(self):
        # Client connection
        self.client = Xively()
        print("Xively connected!")

    def add_value(self, value, time=None):
        if time is None:
            time = datetime.datetime.utcnow().replace(microsecond=0).isoformat()
        self.client.publish_random_value_mqtt(value, time=str(time))

    def get_all(self):
        return self.client.retrieve_random_values_http()

    def get_one(self):
        return self.client.retrieve_random_values_http(page_size=1)


    def get_by_threshold(self, **kwargs):
        result = {}
        all_values = self.get_all()
        for v in all_values:
            if 'max' in kwargs:
                if not 'max' in result:
                    result['max'] = v
                else:
                    if v['value'] > result['max']:
                        result['max'] = v
            if 'min' in kwargs:
                if not 'min' in result:
                    result['min'] = v
                else:
                    if v['value'] > result['min']:
                        result['min'] = v
        return result

class Almacenamiento():
    def __init__(self):
        # Client connection
        self.external_cli = External_DB()
        self.internal_cli = Internal_DB()

        for v in self.external_cli.get_all():
            self.internal_cli.add_value(v['value'], time=v['date'])

    def add_value(self, value):
        self.external_cli.add_value(value)
        self.internal_cli.add_value(value)

    def get_all(self):
        return self.internal_cli.get_all()

    def get_one(self):
        return self.internal_cli.get_one()


    def get_by_threshold(self, **kwargs):
        return self.internal_cli.get_by_threshold(**kwargs)
