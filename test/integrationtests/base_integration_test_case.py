from test import BaseTestCase


class IntegrationBaseTestCase(BaseTestCase):
    newTestUser = {
        'username': 'john',
        'name': 'John',
        'surname': 'Doe',
        'email': 'john@mail.com',
        'tags': 'web development, csse',
        'password': '123456'
    }
    publicTestUser = {
        'username': 'john'
    }
    editTestUser = {
        "name": "ModifiedName",
        "surname": "ModifiedSurname",
        "email": "modified@mail.com",
        "password": "654321",
        "tags": "new tag, second tag"
    }
    newTestIdea = {
        "title": "My Awesome Idea",
        "description": "some description for my fancy idea",
        "category": "web application",
        "tags": "csse, se, agile"
    }
    editTestIdea = {
        "title": "My Awesome Modified Idea",
        "description": "some modified description for my fancy idea",
        "category": "engineering",
        "tags": "csse, web, new tag"
    }
    newTestVote = {
        "value": 1,
        "target": 2
    }
    editTestVote = {
        "value": -1
    }

    api_base_path = '/api/v1'

    @staticmethod
    def attributes_in(object_dict, wrapper_object_dict):
        return set(object_dict.items()).issubset(set(wrapper_object_dict.items()))
