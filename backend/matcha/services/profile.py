from flask import jsonify

from flask_jwt_extended import (
    get_jwt_identity,
)

from matcha.utils import check_request_json

from matcha.db.pictures import db_get_user_images, db_get_url_profile

from matcha.db.visit import db_put_visit, db_get_visit

from matcha.db.fake import db_get_is_faked

from matcha.db.block import db_get_is_blocked

from matcha.db.last_connection import db_get_last_connection

from matcha.db.user import (
    db_set_user_profile_data,
    db_get_user_per_id,
    db_get_user_per_username,
    db_get_username_where_id,
    db_update_by_one_fame_rating,
)

from matcha.db.interests import (
    db_get_interests,
)

from matcha.db.notification import db_put_notification

from matcha.websocket.socket_manager import SocketManager

from matcha.db.like import db_get_is_liked, db_get_list_liked_by

from matcha.utils import check_request_json


def _profile_put(id_user, request):
    json = request.json

    check_request = check_request_json(
        request.headers.get("Content-Type"),
        json,
        ["firstname", "lastname", "selectedGender", "sexualPreference", "bio", "age"],
    )

    if check_request is not None:
        return jsonify(check_request[0]), check_request[1]

    return db_set_user_profile_data(
        json["firstname"],
        json["lastname"],
        json["selectedGender"],
        json["sexualPreference"],
        json["bio"],
        json["age"],
        id_user,
    )


def services_profile(id_user, request):
    id_user = get_jwt_identity()

    if request.method == "PUT":
        error_msg = _profile_put(id_user, request)
        if error_msg:
            return error_msg
        db_update_by_one_fame_rating(id_user)

    user_db = db_get_user_per_id(id_user)
    profile_picture = db_get_url_profile(id_user)
    interests = db_get_interests(id_user)
    liked_by = db_get_list_liked_by(id_user)

    if "url" in profile_picture:
        profile_url = profile_picture["url"]
    elif "error" in profile_picture:
        profile_url = profile_picture["error"]

    return (
        jsonify(
            username=user_db[0],
            email=user_db[1],
            firstname=user_db[2],
            lastname=user_db[3],
            selectedGender=user_db[4],
            sexualPreference=user_db[5],
            bio=user_db[6],
            age=user_db[7],
            email_verified=user_db[8],
            profile_complete=user_db[9],
            fameRating=user_db[10],
            urlProfile=profile_url,
            interests=interests,
            likedBy=liked_by,
            visitedBy=db_get_visit(id_user),
        ),
        200,
    )


def services_profile_username(id_user: int, username: str):
    user_db = db_get_user_per_username(username)

    if user_db is None:
        return (jsonify({"error": "username not found"}), 401)

    interests = db_get_interests(user_db[0])
    pictures = db_get_user_images(user_db[0])
    profile_picture = db_get_url_profile(user_db[0])
    is_liked = db_get_is_liked(id_user, username)

    if "url" in profile_picture:
        profile_url = profile_picture["url"]
    elif "error" in profile_picture:
        profile_url = profile_picture["error"]

    db_put_visit(id_user, user_db[0])

    visitor_username = db_get_username_where_id(id_user)
    db_put_notification(
        id_user, user_db[0], "visit", f"{visitor_username} viewed your profile"
    )

    return (
        jsonify(
            username=user_db[1],
            firstname=user_db[2],
            lastname=user_db[3],
            gender=user_db[4],
            sexualPreference=user_db[5],
            bio=user_db[6],
            age=user_db[7],
            fameRating=user_db[8],
            interests=interests,
            pictures=pictures,
            urlProfile=profile_url,
            isLiked=is_liked,
            connected=SocketManager.is_connected(user_db[0]),
            lastConnection=db_get_last_connection(user_db[0]),
            isFaked=db_get_is_faked(id_user, user_db[0]),
            isBlocked=db_get_is_blocked(id_user, user_db[0]),
        ),
        200,
    )
