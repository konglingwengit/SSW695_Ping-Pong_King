from google.cloud import datastore


def get_all_users():
    # Instantiates a client
    datastore_client = datastore.Client()

    users = list()

    query = datastore_client.query(kind='User')
    query_iter = query.fetch()
    for entity in query_iter:
        email = entity['email']
        key = entity.key.id
        users.append({"email": email, "id": key})

    return users


def user_exists(email: str):
    users = get_all_users()
    for user in users:
        if str(user['email']) == str(email):
            return True
    return False
