from marshmallow import EXCLUDE, Schema, fields
from db import db

class BaseSerializer(Schema):
    class Meta:
        unknown = EXCLUDE



    def __init__(self, *args, **kwargs):
        self.prefetch_data = {}
        self.session = db.session
        self.include = kwargs.pop('include', ())
        self.only = None
        self.exclude = None

        if 'only' in kwargs:
            self.only = kwargs['only']

        if 'exclude' in kwargs:
            self.exclude = kwargs['exclude']

        super().__init__(*args, **kwargs)


    def dump_data(self, records, many=None):
        if many is not None:
            self.many = many

        prefetch_data = records if self.many is True else [records]
        self._add_prefetch_data(prefetch_data)

        return self.dump(records)


    def _add_prefetch_data(self, records):
        pass


    def _add_prefetch_data_model(self, records, key_name, prefetch_key, many=False):   
        self.prefetch_data[prefetch_key] = {}
        prefetched = self.prefetch_data[prefetch_key]

        for record in records:
            key_value = getattr(record, key_name)
            if many:
                if not prefetched.get(key_value):
                    prefetched[key_value] = []
                prefetched[key_value].append(record)
            else:
                if not prefetched.get(key_value):
                    prefetched[key_value] = record



class ModelSerializer(BaseSerializer):
    id = fields.Integer(dump_only=True)



class RoundedFloatField(fields.Float):
    def __init__(self, *, digits = 2, allow_nan: bool = False, as_string: bool = False,**kwargs):
        self.digits = digits
        super().__init__(allow_nan=allow_nan, as_string=as_string, **kwargs)


    def _serialize(self, value, attr, obj, **kwargs):
        value = super()._serialize(value, attr, obj, **kwargs)
        if value is None:
            return value

        return round(value, self.digits)