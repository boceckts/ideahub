def expand_users(queried_users):
    expanded_users = []
    for queried_user in queried_users:
        expanded_users.append(expand_user(queried_user))
    return expanded_users


def expand_user(queried_user):
    user_as_dict = queried_user.as_dict()
    user_as_dict['ideas'] = list(map(lambda idea: idea.id, queried_user.ideas.all()))
    return user_as_dict


def expand_ideas(queried_ideas):
    expanded_ideas = []
    for queried_idea in queried_ideas:
        expanded_ideas.append(expand_idea(queried_idea))
    return expanded_ideas


def expand_idea(queried_idea):
    idea_as_dict = queried_idea.as_dict()
    idea_as_dict['author'] = queried_idea.user_id
    return idea_as_dict
