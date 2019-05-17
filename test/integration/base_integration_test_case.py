from test.base_test_case import BaseTestCase


class IntegrationTestCase(BaseTestCase):
    testNewUserData = {
        'username': 'NewUser',
        'name': 'Name',
        'surname': 'Surname',
        'email': 'name@mail.com',
        'tags': 'web development, csse',
        'password': '123456'
    }
    testEditUserData = {
        "name": "ModifiedName",
        "surname": "ModifiedSurname",
        "email": "modified@mail.com",
        "password": "654321",
        "tags": "new tag, second tag"
    }
    testUserData = {
        "name": "Name",
        "surname": "Surname",
        "email": "name@mail.com",
        "tags": "web development, csse",
        "ideas_count": 0,
        "votes_count": 0,
        "id": 3,
        "username": "NewUser",
        "ideas_url": "http://localhost/api/v1/user/ideas",
        "votes_url": "http://localhost/api/v1/user/votes"
    }
    testNewIdeaData = {
        "title": "New Awesome Idea",
        "description": "some description for my fancy idea",
        "category": "web application",
        "tags": "csse, se, agile"
    }
    testEditIdeaData = {
        "title": "New Awesome Modified Idea",
        "description": "some modified description for my fancy idea",
        "category": "engineering",
        "tags": "csse, web, new tag"
    }
    testNewVoteData = {
        "value": 1,
        "target": 2
    }
    testEditVoteData = {
        "value": -1
    }

    api_base_path = '/api/v1'
