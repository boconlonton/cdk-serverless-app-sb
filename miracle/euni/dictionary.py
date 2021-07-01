from miracle.db import models
from miracle.euni import Abstract


class Dictionary(Abstract):

    key = models.CharField(name='key', max_length=50)
    value = models.CharField(name='value', max_length=20)

    class Meta:
        table_name = 'dictionary'
