from collections import defaultdict
from flask import request
from services.interfaces.ifilters import IFilters
from services.interfaces.ipost_repo import IPostRepo

class Filters(IFilters):
    def __init__(self):
        self.applied = defaultdict()
        self.available = set()
        self.filtered_ids = []
        self.filtered_names = []
    
    def set_newly_applied(self):
        self.applied = defaultdict(lambda: [], request.args.to_dict(flat = False))
        self.filtered_ids = self.applied["user_id"]
        self.filtered_names = self.applied["name"]
        
    def get_new_querystr(self) -> str:
        query_url = request.full_path
        id = request.form.get("user_id")
        name = request.form.get("name")
        query_url = query_url.replace(f"user_id={id}&name={name}&", "")
        return query_url

    def update_available(self, repo : IPostRepo):
        if self.filtered_ids == []:
            self.reset_available(repo)
        for i in range(0, len(self.filtered_ids)):
            self.available.discard((self.filtered_ids[i], self.filtered_names[i]))

    def reset_available(self, posts : IPostRepo):
        result = set()
        for post in posts.get_all(pagination = False):
                result.add((str(post[1].owner_id), post[1].auth))
        self.available = result