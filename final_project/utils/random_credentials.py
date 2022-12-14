from faker import Faker


fake = Faker('ru_RU')


def random_creds():
    username = fake.profile()['username']
    password = fake.password()

    return {'username': username, 'password': password}
