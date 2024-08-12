from pymongo import MongoClient
from pymongo.collection import Collection

#获取MongoDB连接
def  getConnection():
    # client = MongoClient()
    # client = MongoClient('localhost')
    client = MongoClient('localhost', 27017)
    return client

#创建inserOne方法，向数据库中添加一个文档
def  insertOne(collection:Collection, data):
    collection.insert_one(data)

#创建insertMany方法，向数据库中添加多个文档
def  insertMany(collection:Collection, data):
    collection.insert_many(data)

#创建deleteOne方法，删除数据库中满足条件的单个文档
def  deleteOne(collection:Collection, condition):
    collection.delete_one(condition)

#创建deleteMany方法，删除数据库中满足条件的多个文档
def  deleteMany(collection:Collection, condition):
    collection.delete_many(condition)

#创建updateOne方法，更新数据库中满足条件的单个文档
def  updateOne(collection:Collection, condition, data):
    collection.update_one(condition, data)

#创建updateMany方法，更新数据库中满足条件的多个文档
def  updateMany(collection:Collection, condition, data):
    collection.update_many(condition, data)

#创建findOne方法，查询数据库中满足条件的单个文档
def  findOne(collection:Collection, condition):
    return collection.find_one(condition)

#创建findAllCondition方法，查询数据库中满足条件的多个文档
def  findAllCondition(collection:Collection, condition):
    return collection.find(condition)

#创建findAll方法，查询数据库中所有文档
def  findAll(collection:Collection):
    return collection.find()

if __name__ == '__main__':
    pass
