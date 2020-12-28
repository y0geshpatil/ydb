from ydb import yDB
import json

db = yDB('my.db')
name = '{"first name": "yogesh", "last name": "patil"}'
name=json.loads(name)

age = '{"age": 21}'
age=json.loads(age)

db.create("name",name)
db.create("age", age, 60)

print("Name", db.read("name"))
print("Age", db.read("age"))

db.delete("name")

