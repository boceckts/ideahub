from flask import url_for


def expand_users(queried_users):
    expanded_users = []
    for queried_user in queried_users:
        expanded_user = expand_user(queried_user)
        if expanded_user is not None:
            expanded_users.append(expanded_user)
    return expanded_users


def expand_user(queried_user):
    if queried_user is not None:
        user_as_dict = queried_user.as_dict()
        user_as_dict['ideas_url'] = url_for('user_ideas_ep', user_id=queried_user.id, _external=True)
        user_as_dict['votes_url'] = url_for('user_votes_ep', user_id=queried_user.id, _external=True)
        user_as_dict['ideas_count'] = len(queried_user.ideas.all())
        user_as_dict['votes_count'] = len(queried_user.votes.all())
        return user_as_dict


def expand_ideas(queried_ideas):
    expanded_ideas = []
    for queried_idea in queried_ideas:
        expanded_idea = expand_idea(queried_idea)
        if expanded_idea is not None:
            expanded_ideas.append(expanded_idea)
    return expanded_ideas


def expand_idea(queried_idea):
    if queried_idea is not None:
        idea_as_dict = queried_idea.as_dict()
        idea_as_dict['author'] = queried_idea.user_id
        idea_as_dict['votes_count'] = queried_idea.votes_count
        idea_as_dict['score'] = queried_idea.score
        idea_as_dict['upvotes'] = queried_idea.upvotes
        idea_as_dict['downvotes'] = queried_idea.downvotes
        idea_as_dict['votes_url'] = url_for('idea_votes_ep', idea_id=queried_idea.id, _external=True)
        return idea_as_dict


def expand_votes(queried_votes):
    expanded_votes = []
    for queried_vote in queried_votes:
        expanded_vote = expand_vote(queried_vote)
        if expanded_vote is not None:
            expanded_votes.append(expanded_vote)
    return expanded_votes


def expand_vote(queried_vote):
    if queried_vote is not None:
        vote_as_dict = queried_vote.as_dict()
        vote_as_dict['target'] = queried_vote.idea_id
        vote_as_dict['owner'] = queried_vote.user_id
        return vote_as_dict
