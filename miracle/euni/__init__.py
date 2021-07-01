from collections import namedtuple

from miracle.db import models


Fields = namedtuple('Fields', 'name type extra_context')


class Abstract(models.Model):
    created_by = models.ForeignKey(
        ref_table='user',
        ref_column='id',
        on_delete_cascade=True
    )
    updated_by = models.ForeignKey(
        ref_table='user',
        ref_column='id',
        on_delete_cascade=True
    )
    created_at = models.DateTimeField(default_now=True)
    updated_at = models.DateTimeField(default_now=True)
