from flask import Blueprint, render_template
from services.dependency_inject.injector import Services
from services.interfaces.iauthorization import IAuthorization
from services.interfaces.isession_mngr import ISessionMNGR
from services.interfaces.iuser_statistics import IUserStatistics
from services.interfaces.iusers_repo import IUsersRepo
from services.users.access_decorators import AccessDecorators

class Statistics:
    access = AccessDecorators(IAuthorization, ISessionMNGR)

    @Services.get
    def __init__(self, statistics : IUserStatistics):
        self.statistics = statistics
        self.bp = Blueprint("statistics",  __name__)
        self.get_statistic = self.register("/statistics/<id>/", self.get_statistic)
        
    def register(self, link, func):
        return self.bp.route(link, methods = ["Get", "Post"])(func)

    @access.member_required
    def get_statistic(self, id):
        return render_template("statistics.html", table = self.statistics.get(id))
