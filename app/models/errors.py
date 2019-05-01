class IdeaNotFoundError(Exception):
    def __init__(self):
        Exception.__init__(self)
        self.message = 'The idea could not be found.'


class VoteExistsError(Exception):
    def __init__(self):
        Exception.__init__(self)
        self.message = 'The vote already exists.'
