from flask import Flask
from pytest import fixture
from services.users.users_in_memo import Users

from tests.helpers import add_disposable_user, configure, log_user


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
def test_statistics_displays_posts_for_one_month_old_users(client):
    user_id = add_disposable_user()
    Users().get_by(id = user_id).created = "17/May/22 11:32:25"
    read_stats = client.get(f"/user/statistics/{user_id}/")
    assert "<td>May/22</td>" in read_stats.data.decode("UTF-8")
    assert "<td>Jun/22</td>" in read_stats.data.decode("UTF-8")
    client.post(f"view/{user_id}/?pg=1", data = {"userID" : user_id})

@log_user(1, "Mark", "Mark@mail", "regular")
@configure(True)
def test_statistics_displays_posts_count_older_users(client):
    Users().get_by(id = "1").created = "17/Mar/22 11:32:25"
    read_stats = client.get(f"/user/statistics/1/")
    assert "<td>Mar/22</td>" in read_stats.data.decode("UTF-8")
    assert "<td>Apr/22</td>" in read_stats.data.decode("UTF-8")
    assert "<td>May/22</td>" in read_stats.data.decode("UTF-8")
    assert "<td>Jun/22</td>" in read_stats.data.decode("UTF-8")
