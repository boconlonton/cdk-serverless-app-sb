from miracle.db import models
from miracle.euni import Abstract


class User(Abstract):
    first_name = models.CharField(name='fname', max_length=30,
                                  min_length=10, default='Tan')
    last_name = models.CharField(max_length=30, nullable=False)

    class Meta:
        table_name = 'user'

    def __init__(self, *, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def validate(self):
        pass

    def save(self, *, instance=None, **kwargs):
        if instance:
            pass
        else:
            pass
