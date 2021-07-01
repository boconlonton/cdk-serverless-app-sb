"""
This module defines the SQL DDL Script which then be used for create database
"""

from miracle.euni.users import User
from miracle.euni.dictionary import Dictionary


scripts = User.generate_ddl_scripts()
scripts += f'\n{Dictionary.generate_ddl_scripts()}'
print(scripts)
