from flask import Flask
from pytest import fixture
from services.users.users_in_memo import Users

from tests.helpers import configure, log_user

@fixture()
def client(data_base : Flask):
    return data_base.test_client()

@log_user(1, "Mark", "Mark@mail", "regular")
@configure(True)
def test_onefield_only_if_user_created_this_month(client):
    read_stats = client.get("/user/statistics/1/")
    assert (
    "<th>No.ofposts</th>\n</tr>\n\n<tr>\n<td>Jun/22</td>\n<td>3</td>\n</tr>\n\n</table>\n"
    in read_stats.data.decode("UTF-8").replace(" ", ""))

@log_user(1, "Mark", "Mark@mail", "regular")
@configure(True)
def test_statistics_displayed_correctly_for_one_month_user(client):
    read_stats = client.get("/user/statistics/1/")
    assert "<td>Jun/22</td>\n<td>3</td>\n" in read_stats.data.decode("UTF-8").replace(" ", "")

@log_user(1, "Mark", "Mark@mail", "regular")
@configure(True)
def test_statistics_displays_only_months_with_activity(client):
    Users().get_by(id = "1").created = "17/Mar/22 11:32:25"
    read_stats = client.get(f"/user/statistics/1/")
    assert "<td>Jun/22</td>" in read_stats.data.decode("UTF-8")
