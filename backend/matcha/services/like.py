from flask import jsonify

from matcha.utils import get_id_where_username_else_error

from matcha.db.user import db_get_username_where_id

from matcha.utils import check_request_json_values

from matcha.db.user import db_get_id_where_username
from matcha.db.user import db_get_username_where_id
from matcha.utils import check_request_json_values

from matcha.db.user import db_get_id_where_username
from matcha.db.user import db_get_username_where_id
from matcha.db.user import db_update_by_one_fame_rating

from matcha.db.notification import db_put_notification

from matcha.db.like import (
    db_put_unlike_user,
    db_put_like_user,
    db_get_list_liked_by,
    db_get_is_liked,
)


def services_like_user_get(id_user):
    return db_get_list_liked_by(id_user)


def services_like_user(id_user, request):
    if request.method == "GET":
        likers = services_like_user_get(id_user)
        return jsonify({"likers": likers}), 201

    json = request.json

    username = None

    if "like" in json:
        username = json["like"]
        error = db_put_like_user(id_user, json["like"])
        if error is not None:
            return error

        id_to_notify = get_id_where_username_else_error(json["like"])
        db_update_by_one_fame_rating(id_to_notify)
        if not isinstance(id_to_notify, int):
            return id_to_notify

        liker_username = db_get_username_where_id(id_user)

        title = "like"
        content = f"{liker_username} like you"

        db_put_notification(id_user, id_to_notify, title, content)

    elif "unlike" in json:
        username = json["unlike"]
        error = db_put_unlike_user(id_user, json["unlike"])

        id_to_notify = get_id_where_username_else_error(json["unlike"])
        if not isinstance(id_to_notify, int):
            return id_to_notify

        liker_username = db_get_username_where_id(id_user)

        title = "unlike"
        content = f"{liker_username} unlike you"
        db_put_notification(id_user, id_to_notify, title, content)
    else:
        return jsonify({"error": "bad payload"}), 400

    if error is not None:
        return error

    is_liked = db_get_is_liked(id_user, username)
    return jsonify({"isLiked": is_liked}), 201
