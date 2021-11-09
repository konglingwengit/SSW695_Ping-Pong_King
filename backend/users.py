from typing import Dict
from google.cloud import datastore

input_users: Dict = dict()
client = None


def get_all_users():
    global input_users
    if len(input_users) == 0:
        # Normal path

        # Instantiates a client
        datastore_client = datastore.Client()

        users = list()

        query = datastore_client.query(kind='User')
        query_iter = query.fetch()
        for entity in query_iter:
            email = entity['email']
            key = entity.key.id
            users.append({"email": email, "id": key})

    else:
        # Used for unit testing
        users = input_users

    return users


def user_exists(email: str):
    users = get_all_users()
    for user in users:
        if str(user['email']) == str(email):
            return True
    return False

def add_user(email: str):
    global client
    if client is None:
        client = datastore.Client()
    entity = datastore.entity.Entity()
    entity.key = client.key('User')
    entity['email'] = email
    client.put(entity)