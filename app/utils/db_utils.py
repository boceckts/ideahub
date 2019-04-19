def expand_users(queried_users):
    expanded_users = []
    for queried_user in queried_users:
        expanded_users.append(expand_user(queried_user))
    return expanded_users


def expand_user(queried_user):
    user_as_dict = queried_user.as_dict()
    user_as_dict['ideas'] = list(map(lambda idea: idea.id, queried_user.ideas.all()))
    return user_as_dict
