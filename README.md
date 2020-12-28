# yDB
yDB is file-based and key-value pair data store that support tha basic CRD (create,read and delete) operation.

## ydb.py
Source code
## test.py
Test code

## yDB Functions
```python
>>> from ydb import yDB

#create object of database
>>> db = yDB('<file_name>.db')

#add new key-value pair, return error if key alredy exist
>>> db.create('<key>', <value>, [<time_live_property>]) # time_live_property is optional parameter

#read value for given key, return error if key does not 
>>> db.read('<key>')

#delete key-value for given key, return error if key does not 
>>> db.delete('<key>')

```
