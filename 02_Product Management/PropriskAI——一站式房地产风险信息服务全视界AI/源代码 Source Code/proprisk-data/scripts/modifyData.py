from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['gongyingshang']

if __name__ == '__main__':
    collection = db['Affected_Suppliers_List']
    cursor = collection.find({})
    for document in cursor:
        new_source = ''
        if document['出处来源'] == 'xinlangcaijing':
            new_source = '新浪财经'
        elif document['出处来源'] == 'touzizhe':
            new_source = '投资者问答'
        elif document['出处来源'] == 'yanbao':
            new_source = '研报'

        if new_source:
            collection.update_one({'_id': document['_id']}, {'$set': {'出处来源': new_source}})
            print(f"文档 {document['_id']} 更新完毕！")

    print('更新完毕！')
