from flask import request, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)

from matcha.app_utils import check_request_json

from matcha.db.db import (
    db_get_interests,
    db_get_user_images,
    db_set_user_profile_data,
    db_get_user_per_id,
    db_get_user_per_username,
    db_get_url_profile,
)

from matcha.db.like import db_get_is_liked, db_get_list_liked_by

from matcha.app_utils import check_request_json


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

    get_username = request.args.get("username", default="", type=str)

    if get_username == "":
        user_db = db_get_user_per_id(id_user)
        profile_picture = db_get_url_profile(id_user)
        interests = db_get_interests(id_user)
        liked_by = db_get_list_liked_by(id_user)

        if "url" in profile_picture:
            profile_url = url = profile_picture["url"]
        elif "error" in profile_picture:
            profile_url = url = profile_picture["error"]

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
            ),
            200,
        )
    else:
        user_db = db_get_user_per_username(get_username)
        interests = db_get_interests(user_db[0])
        pictures = db_get_user_images(user_db[0])
        profile_picture = db_get_url_profile(user_db[0])
        is_liked = db_get_is_liked(id_user, get_username)

        if "url" in profile_picture:
            profile_url = url = profile_picture["url"]
        elif "error" in profile_picture:
            profile_url = url = profile_picture["error"]

        if user_db is None:
            return (jsonify({"error": "username not found"}), 401)

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
            ),
            200,
        )