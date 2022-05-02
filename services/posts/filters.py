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
        
    def apply(self, query_params : dict, page : int) -> list:
        ids = []
        if len(self.repo) > 0 :
            self.set_newly_applied(query_params)
            self.update_available()
            ids += self.applied["user_id"]
            return self.repo.get_all(page, ids)
        else:
            return placeholder.get_all()

    def set_newly_applied(self, query_params : dict):
        self.applied = defaultdict(lambda: [], query_params)
        
    def get_new_querystr(self) -> str:
        query_url = request.full_path
        id = request.form.get("user_id")
        name = request.form.get("name")
        query_url = query_url.replace(f"user_id={id}&name={name}&", "")
        return query_url

    def update_available(self):
        if len(self.applied) == 0:
            self.reset_available()
        for keys in self.applied:
            for items in self.applied[keys]:
                self.available.discard((keys, items))

    def reset_available(self):
        result = set()
        i = 0
        for post in self.repo.get_all():
            result.add((str(post[1].owner_id), post[1].auth))
        self.available = result
        