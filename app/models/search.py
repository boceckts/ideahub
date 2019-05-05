class Search:
    title = 'any'
    category = 'any'
    tags = 'any'

    @staticmethod
    def of_form(form):
        search = Search()
        search.title = form.title.data
        search.category = form.category.data
        search.tags = form.tags.data
        return search
