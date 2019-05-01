from app.models import Idea


def get_idea(idea_id):
    return Idea.query.get(idea_id)
