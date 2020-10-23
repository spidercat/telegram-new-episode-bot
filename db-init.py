from tinydb import TinyDB, Query, where

db = TinyDB('tinydb/db.json')

groups = db.table('groups')
config = db.table('config')

q = config.search(Query().token.exists())[0]
print(q)
exit()

groups.insert({'whoami': {'Maxim': 'Ты отец.', 'Ola': 'Мать ты.', 'Nitay': 'You are nagging, little monster. Also known as Nitay.', 'Ido': 'You\'re esteemed guest of Grabarnik family bot.'}})
groups.insert({'name': 'Maxim', 'chat_id': '898147660'})
groups.insert({'name': 'Ola', 'chat_id': '930059357'})
groups.insert({'name': 'Nitay', 'chat_id': '802580898'})
groups.insert({'name': 'Idan', 'chat_id': '1142897890'})
groups.insert({'name': 'Naama', 'chat_id': '1171727092'})

# db.insert({'name': 'Family', 'members': ['898147660', '930059357', '1142897890', '1142897890', '1171727092']})
# db.insert({'name': 'Admins', 'members': ['898147660', '930059357']})
# db.insert({'name': 'Kids Quorum', 'members': ['1142897890', '1142897890', '1171727092']})

# q = db.search(where('name') == 'Family')
# print(q[0]['members'])
# print( '898147660' in q[0]['members'])


# table.insert({'name': 'Maxim', 'chat_id': '898147660'})
# table.insert({'name': 'Ola', 'chat_id': '930059357'})
# table.insert({'name': 'Nitay', 'chat_id': '802580898'})
# table.insert({'name': 'Idan', 'chat_id': '1142897890'})
# table.insert({'name': 'Naama', 'chat_id': '1171727092'})

config.insert({'token': "123456789"})


# username: None
# first_name: Maxim
# last_name: None
# chat id : 898147660
# username: None
# first_name: ola
# last_name: None
# chat id : 930059357
# username: None
# first_name: Nitay
# last_name: None
# chat id : 802580898
# username: None
# first_name: Idan
# last_name: None
# chat id : 1142897890
# username: None
# first_name: Naama
# last_name: None
# chat id : 1171727092
