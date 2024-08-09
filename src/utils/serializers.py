from rest_framework import serializers
from abc import ABC


class BaseLogsSerizalizer:
    pass


class BaseModelSerializer:

    def validate(self, data):
        if self.instance is not None:
            for field, value in data.items():
                setattr(self.instance, field, value)

            self.instance.full_clean()
        else:
            obj = self.__class__.Meta.model(**data)
            obj.full_clean()

        return data
