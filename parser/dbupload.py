import uuid

from pymongo import MongoClient

db_uri = '185.178.46.173'
# db_uri = 'localhost'
user_pass = 'root:root'
db_port = '27017'

client = MongoClient(f'mongodb://{user_pass}@{db_uri}:{db_port}/')
col_food = client['flame-api']['foods']
col_types = client['flame-api']['foods_types']


with open('foods.txt', 'r') as f:
    result = f.read().splitlines()

count = 0
typeres = []

print('Upload into collection foods has started\n')
for res in result:
    post = {}
    post['image'] = None

    if 'type:' in res:
        count += 1
        typename = res.replace('type: ', '')
        typeres.append({'title': typename, 'group_id': count})
    else:
        splited = res.split(' ')
        title = ' '.join(splited[:-4])
        calories, proteins, fats, carbohydrates = splited[-4:]

        post['id'] = str(uuid.uuid4().hex)
        post['group_id'] = count
        post['title'] = title
        post['carbohydrates'] = float(carbohydrates.replace(',', '.'))
        post['fats'] = float(fats.replace(',', '.'))
        post['proteins'] = float(proteins.replace(',', '.'))
        post['calories'] = int(float(calories.replace(',', '.')))

        col_food.insert_one(post)

        print(f'uploaded: {post}')

print('Upload into collection foods complete\n')
print('Created index: group_id/id\n')
col_food.create_index('group_id')
col_food.create_index('id')

print('Upload into collection foods_types has started\n')
for types in typeres:
    col_types.insert_one(types)
    print(f'uploaded: {types}')
print('Upload into collection foods_types complete\n')

print('Created index: group_id\n')
col_types.create_index('group_id')
