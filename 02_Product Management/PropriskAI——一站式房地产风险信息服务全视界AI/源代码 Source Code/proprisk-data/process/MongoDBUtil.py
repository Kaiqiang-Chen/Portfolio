from pymongo import MongoClient
from pymongo.collection import Collection

#��ȡMongoDB����
def  getConnection():
    # client = MongoClient()
    # client = MongoClient('localhost')
    client = MongoClient('localhost', 27017)
    return client

#����inserOne�����������ݿ������һ���ĵ�
def  insertOne(collection:Collection, data):
    collection.insert_one(data)

#����insertMany�����������ݿ�����Ӷ���ĵ�
def  insertMany(collection:Collection, data):
    collection.insert_many(data)

#����deleteOne������ɾ�����ݿ������������ĵ����ĵ�
def  deleteOne(collection:Collection, condition):
    collection.delete_one(condition)

#����deleteMany������ɾ�����ݿ������������Ķ���ĵ�
def  deleteMany(collection:Collection, condition):
    collection.delete_many(condition)

#����updateOne�������������ݿ������������ĵ����ĵ�
def  updateOne(collection:Collection, condition, data):
    collection.update_one(condition, data)

#����updateMany�������������ݿ������������Ķ���ĵ�
def  updateMany(collection:Collection, condition, data):
    collection.update_many(condition, data)

#����findOne��������ѯ���ݿ������������ĵ����ĵ�
def  findOne(collection:Collection, condition):
    return collection.find_one(condition)

#����findAllCondition��������ѯ���ݿ������������Ķ���ĵ�
def  findAllCondition(collection:Collection, condition):
    return collection.find(condition)

#����findAll��������ѯ���ݿ��������ĵ�
def  findAll(collection:Collection):
    return collection.find()

if __name__ == '__main__':
    pass
