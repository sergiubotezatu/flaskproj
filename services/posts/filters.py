from collections import defaultdict
from flask import request
from services.dependency_inject.injector import Services
from services.interfaces.ifilters import IFilters
from services.interfaces.ipost_repo import IPostRepo
from services.posts.seed import placeholder

class Filters(IFilters):
    @Services.get
    def __init__(self, repo : IPostRepo):
        self.repo = repo
        self.applied = defaultdict()
        self.available = set()
        self.filtered_ids = []
        self.filtered_names = []

    def apply(self, query_params : dict, page : int) -> list:
        if len(self.repo) > 0 :
            self.set_newly_applied(query_params)
            self.update_available()
            return self.repo.get_all(page, self.filtered_ids)
        else:
            return placeholder.get_all()

    def set_newly_applied(self, query_params : dict):
        self.applied = defaultdict(lambda: [], query_params)
        self.filtered_ids = self.applied["user_id"]
        self.filtered_names = self.applied["name"]
        
    def get_new_querystr(self) -> str:
        query_url = request.full_path
        id = request.form.get("user_id")
        name = request.form.get("name")
        query_url = query_url.replace(f"user_id={id}&name={name}&", "")
        return query_url

    def update_available(self):
        if self.filtered_ids == []:
            self.reset_available()
        for i in range(0, len(self.filtered_ids)):
            self.available.discard((self.filtered_ids[i], self.filtered_names[i]))

    def reset_available(self):
        result = set()
        for post in self.repo.get_all():
                result.add((str(post[1].owner_id), post[1].auth))
        self.available = result
