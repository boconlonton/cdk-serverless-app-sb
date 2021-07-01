import inspect
from decimal import Decimal
from typing import Optional, ClassVar


class Model:

    @classmethod
    def get_all_attributes(cls):
        attributes = inspect.getmembers(
            cls, lambda a: not (inspect.isroutine(a))
        )
        return (
            a for a in attributes
            if not(a[0].startswith('__') and a[0].endswith('__'))
        )

    @classmethod
    def generate_ddl_scripts(cls):
        rows = ['id BIGSERIAL PRIMARY KEY']
        for attr in cls.get_all_attributes():
            if attr[0] == 'Meta':
                continue
            if getattr(attr[1], '_name'):
                script = attr[1].to_ddl_script()
            else:
                script = f'{attr[0]} {attr[1].to_ddl_script()}'
            rows.append(script)
        temp = ',\n\t'.join(rows)
        schema = ''
        table_name = cls.__name__
        if getattr(cls, 'Meta', None):
            table_name = cls.Meta.table_name \
                if getattr(cls.Meta, 'table_name', None) else cls.__name__
            schema = f"'{cls.Meta.db_schema}'." \
                if getattr(cls.Meta, 'db_schema', None) else ''
        return f"CREATE TABLE {schema}{table_name} (\n\t{temp}\n);"


class Field:

    def __init__(self, *, nullable: bool = False, unique: bool = False):
        self.nullable = nullable
        self.unique = unique
        self._null_script = ' NOT NULL' if not nullable else ''
        self._unique_script = ' UNIQUE' if not unique else ''

    @property
    def nullable(self):
        return self._nullable

    @nullable.setter
    def nullable(self, value):
        self._nullable = value

    @property
    def unique(self):
        return self._unique

    @unique.setter
    def unique(self, value):
        self._unique = value


class CharField(Field):

    def __init__(self, name: str = None, max_length: int = None,
                 min_length: int = None, nullable: bool = False,
                 unique: bool = False, default: str = None):
        super().__init__(nullable=nullable, unique=unique)
        self._name = name
        self._max_length = max_length
        self._min_length = min_length
        self.default_value = default

    @property
    def default_value(self):
        return self._default

    @default_value.setter
    def default_value(self, value):
        self._default = value
        if self._default:
            self._default_script = f" DEFAULT '{self._default}'"
        else:
            self._default_script = ''

    def to_ddl_script(self):
        if self._max_length:
            data_type = f'varchar({self._max_length})'
        else:
            data_type = 'varchar(255)'
        script = f'{data_type}{self._default_script}' \
                 f'{self._null_script}{self._unique_script}'
        if self._name:
            return f'{self._name} {script}'
        else:
            return f'{script}'


class IntegerField(Field):

    def __init__(self, name: str = None, min_value: int = None,
                 max_value: int = None, nullable: bool = False,
                 unique: bool = False, default: int = None):
        super().__init__(nullable=nullable, unique=unique)
        self._name = name
        self._min_value = min_value
        self._max_value = max_value
        self.default_value = default

    @property
    def default_value(self):
        return self._default

    @default_value.setter
    def default_value(self, value):
        self._default = value
        if self._default:
            self._default_script = f" DEFAULT '{self._default}'"
        else:
            self._default_script = ''

    def to_ddl_script(self):
        script = f'INT{self._default_script}' \
                 f'{self._null_script}{self._unique_script}'
        if self._name:
            return f'{self._name}{script}'
        else:
            return f'{script}'


class DecimalField(Field):

    def __init__(self, name: str = None, min_value: Decimal = None,
                 max_value: Decimal = None, nullable: bool = False,
                 unique: bool = False, decimal_places: int = None,
                 default: Decimal = None):
        super().__init__(nullable=nullable, unique=unique)
        self._name = name
        self._min_value = min_value
        self._max_value = max_value
        self._decimal_places = decimal_places
        self.default_value = default

    @property
    def default_value(self):
        return self._default

    @default_value.setter
    def default_value(self, value):
        self._default = value
        if self._default:
            self._default_script = f" DEFAULT '{self._default}'"
        else:
            self._default_script = ''

    def to_ddl_script(self):
        script = f'REAL{self._default_script}' \
                 f'{self._null_script}{self._unique_script}'
        if self._name:
            return f'{self._name}{script}'
        else:
            return f'{script}'


class DateField(Field):

    def __init__(self, name: str = None, min_date: str = None,
                 max_date: str = None, nullable: bool = False,
                 unique: bool = False, format_date: str = '%Y-%m-%d',
                 default_now: bool = False):
        super().__init__(nullable=nullable, unique=unique)
        self._name = name
        self._min_date = min_date
        self._max_date = max_date
        self._format_date = format_date
        self.default_now = default_now

    @property
    def default_now(self):
        return self._default_now

    @default_now.setter
    def default_now(self, value):
        self._default_now = value
        if value:
            self._default_script = f' DEFAULT ' \
                                   f'EXTRACT(EPOCH FROM CURRENT_TIMESTAMP)'
        else:
            self._default_script = ''

    def to_ddl_script(self):
        script = f'BIGINT{self._default_script}' \
                 f'{self._null_script}{self._unique_script}'
        if self._name:
            return f'{self._name}{script}'
        else:
            return f'{script}'


class DateTimeField(Field):

    def __init__(self, name: str = None, min_date: str = None,
                 max_date: str = None, nullable: bool = False,
                 unique: bool = False, format_date: str = '%Y-%m-%d %H:%M:%S',
                 default_now: bool = False):
        super().__init__(nullable=nullable, unique=unique)
        self._name = name
        self._min_date = min_date
        self._max_date = max_date
        self._format_date = format_date
        self.default_now = default_now

    @property
    def default_now(self):
        return self._default_now

    @default_now.setter
    def default_now(self, value):
        self._default_now = value
        if value:
            self._default_script = f' DEFAULT ' \
                                   f'EXTRACT(EPOCH FROM CURRENT_TIMESTAMP)'
        else:
            self._default_script = ''

    def to_ddl_script(self):
        script = f'BIGINT{self._default_script}' \
                 f'{self._null_script}{self._unique_script}'
        if self._name:
            return f'{self._name}{script}'
        else:
            return f'{script}'


class ForeignKey(Field):

    def __init__(self, *, ref_column: str, ref_class: ClassVar = None,
                 ref_table: str = None, name: str = None, default: str = None,
                 unique: bool = False, nullable: bool = False,
                 on_delete_cascade=True):
        super().__init__(nullable=nullable, unique=unique)
        self.default_value = default
        self._name = name
        self._ref_class = ref_class
        self._ref_table = ref_table
        self._ref_column = ref_column
        if isinstance(default, str):
            self._default_script = f"DEFAULT '{default}'"
        elif isinstance(default, int):
            self._default_script = f"DEFAULT {default}"
        if on_delete_cascade:
            self._cascade_script = ' ON DELETE CASCADE'
        else:
            self._cascade_script = ''

    def to_ddl_script(self):
        if self._ref_class:
            table_name = getattr(self._ref_class.Meta, 'table_name')
        else:
            table_name = self._ref_table
        script = f'INT REFERENCES {table_name} ({self._ref_column})' \
                 f'{self._cascade_script}'
        if self._name:
            return f'{self._name}{script}'
        else:
            return f'{script}'
