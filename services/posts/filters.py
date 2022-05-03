from collections import defaultdict
from flask import request
from services.dependency_inject.injector import Services
from services.interfaces.ifilters import IFilters
from services.interfaces.ipost_repo import IPostRepo
from services.posts.seed import placeholder

class Filters(IFilters):
    __is_first_access = True

    @Services.get
    def __init__(self, repo : IPostRepo):
        self.repo = repo
        self.filtered_users = defaultdict()
        self.unfiltered_users = set()
        
    def apply(self, query_params : dict, page : int) -> list:
        ids = []
        if len(self.repo) > 0 :
            self.__build_initial_unfiltered()
            self.filtered_users = defaultdict(lambda: [], query_params)
            self.__update_unfiltered_users()
            ids += self.filtered_users["user_id"]
            return self.repo.get_all(page, ids)
        else:
            return placeholder.get_all()

    def get_new_querystr(self) -> str:
        query_url = request.full_path
        id = request.form.get("user_id")
        name = request.form.get("name")
        query_url = query_url.replace(f"user_id={id}&name={name}&", "")
        self.unfiltered_users.add((id, name))
        return query_url

    def __update_unfiltered_users(self):
        if len(self.filtered_users) > 0:
            ids = self.filtered_users["user_id"]
            names = self.filtered_users["name"]
            for i in range(0, len(ids)):
                self.unfiltered_users.discard((ids[i], names[i]))
        else:
            self.__reset_unfiltered_users()        
            
    def __reset_unfiltered_users(self) -> set:
        result = set()
        for post in self.repo.get_all():
            result.add((str(post[1].owner_id), post[1].auth))
        self.unfiltered_users = result

    def __build_initial_unfiltered(self):
        if Filters.__is_first_access:
            self.__reset_unfiltered_users()
            Filters.__is_first_access = True
        