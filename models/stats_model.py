from collections import defaultdict

class StatisticsModel:
    def __init__(self, username : str, posts_per_month : defaultdict[str , int]):
        self.username = username
        self.posts_per_month = posts_per_month
        
