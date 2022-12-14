import allure
import faker

from data_models.user_model import User

fake = faker.Faker('ru_RU')


@allure.step('Создание пользовательских данных')
def full_user(name_min_len=None, surname_min_len=None, middle_name_min_len=None, username_min_len=None,
              password_len=None, email_min_len=None):

    if name_min_len is None:
        name = fake.first_name()
    else:
        name = ''
        while len(name) < name_min_len:
            name += f'{fake.first_name()} '
        if len(name) > name_min_len:
            name = name[:name_min_len]

    if surname_min_len is None:
        surname = fake.first_name()
    else:
        surname = ''
        while len(surname) < surname_min_len:
            surname += f'{fake.last_name()} '
        if len(surname) > surname_min_len:
            surname = surname[:surname_min_len]

    if middle_name_min_len is None:
        middle_name = fake.first_name()
    else:
        middle_name = ''
        while len(middle_name) < middle_name_min_len:
            middle_name += f'{fake.middle_name()} '
        if len(middle_name) > middle_name_min_len:
            middle_name = middle_name[:middle_name_min_len]

    if username_min_len is None:
        username = fake.profile()['username']
    else:
        username = ''
        while len(username) < username_min_len:
            username += f'{fake.profile()["username"]} '
        if len(username) > username_min_len:
            username = username[:username_min_len]

    password = fake.password(length=password_len or 7)

    if email_min_len is None:
        email = fake.safe_email()
    elif email_min_len < 15:
        left_len = email_min_len - 4
        left = 'a' * left_len
        email = left + '@a.a'
    else:
        domain = f'@{fake.safe_domain_name()}'
        left_len = email_min_len - len(domain)
        left = ''
        while len(left) < left_len:
            left += fake.lexify('?')
        email = left + domain

    return User(name=name,
                surname=surname,
                middle_name=middle_name,
                username=username,
                password=password,
                email=email).__dict__


def user_without_name():
    user = full_user()
    user.pop('name')

    return user


def user_without_surname():
    user = full_user()
    user.pop('surname')

    return user


def user_without_middle_name():
    user = full_user()
    user.pop('middle_name')

    return user


def user_without_username():
    user = full_user()
    user.pop('username')

    return user


def user_without_email():
    user = full_user()
    user.pop('email')

    return user


def user_without_password():
    user = full_user()
    user.pop('password')

    return user
