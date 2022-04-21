from collections import defaultdict
from flask import request
from services.interfaces.ifilters import IFilters
from services.interfaces.ipost_repo import IPostRepo

class Filters(IFilters):
    def __init__(self):
        self.filters = defaultdict()
        self.not_filtered = set()
        self.ids = []
        self.names = []
    
    def set_current_filters(self):
        self.filters = defaultdict(lambda: [], request.args.to_dict(flat = False))
        self.ids = self.filters["user_id"]
        self.names = self.filters["name"]
        
    def get_new_path(self) -> str:
        query_url = request.full_path
        id = request.form.get("user_id")
        name = request.form.get("name")
        query_url = query_url.replace(f"user_id={id}&name={name}&", "")
        return query_url

    def update_not_filtered(self, repo):
        if self.ids == []:
            self.set_not_filtered(repo)
        for i in range(0, len(self.ids)):
            self.not_filtered.discard((self.ids[i], self.names[i]))

    def set_not_filtered(self, posts : IPostRepo) -> set:
        result = set()
        for post in posts.get_all(pagination = False):
                result.add((str(post[1].owner_id), post[1].auth))
        self.not_filtered = result