#!/bin/python

from test_utils import (
    check_login_token,
    check_415,
    check_get,
    check_post,
    check_put,
    check_put_token,
    check_post_token,
    check_get_token,
    check_get_token_pictures,
    check_post_token_pictures,
    check_put_token_pictures,
    check_delete_token,
    check_delete_token_body,
    confirm_get_last_url,
)

HTTP_405 = b"<!doctype html>\n<html lang=en>\n<title>405 Method Not Allowed</title>\n<h1>Method Not Allowed</h1>\n<p>The method is not allowed for the requested URL.</p>\n"


def test_create_another_user():
    check_post(
        "/api/register",
        200,
        {
            "username": "another",
            "firstname": "Another",
            "lastname": "User",
            "email": "another@flask.py",
            "password": "5678",
        },
        {"success": "User another was successfully added"},
    )
    check_login_token(
        "/api/login",
        {"username": "another", "password": "5678"},
    )
    check_put_token(
        "/api/profile",
        200,
        {
            "age": "18",
            "firstname": "Another",
            "lastname": "User",
            "selectedGender": "m",
            "sexualPreference": "e",
            "bio": "My bio is short. with special a single quote '",
        },
        {
            "age": 18,
            "bio": "My bio is short. with special a single quote '",
            "email": "another@flask.py",
            "email_verified": False,
            "fameRating": 0,
            "firstname": "Another",
            "interests": [],
            "lastname": "User",
            "likedBy": [],
            "profile_complete": True,
            "selectedGender": "m",
            "sexualPreference": "e",
            "urlProfile": "no url",
            "username": "another",
            "visitedBy": [],
        },
    )


def test_register():
    check_415("/api/register")
    check_get("/api/register", 405, HTTP_405)
    check_post(
        "/api/register",
        200,
        {
            "username": "user",
            "firstname": "firstname",
            "lastname": "lastname",
            "email": "email@email.com",
            "password": "1234",
        },
        {"success": "User user was successfully added"},
    )

    check_post(
        "/api/register",
        400,
        {
            "username": "user",
            "lastname": "lastname",
            "email": "email@email.com",
            "password": "1234",
        },
        {"error": "The following fields are required and cannot be empty: firstname"},
    )

    check_post(
        "/api/register",
        400,
        {
            "firstname": "firstname",
            "lastname": "lastname",
            "email": "email@email.com",
            "password": "1234",
        },
        {"error": "The following fields are required and cannot be empty: username"},
    )

    check_post(
        "/api/register",
        401,
        {
            "username": "user",
            "firstname": "firstname",
            "lastname": "lastname",
            "email": "email@email.com",
            "password": "1234",
        },
        {"error": "User user is already registered."},
    )

    check_post(
        "/api/register",
        400,
        {
            "username": "",
            "firstname": "firstname",
            "lastname": "lastname",
            "email": "email@email.com",
            "password": "1234",
        },
        {"error": "The following fields are required and cannot be empty: username"},
    )

    check_post(
        "/api/register",
        400,
        {
            "username": "user",
            "firstname": "",
            "lastname": "lastname",
            "email": "email@email.com",
            "password": "1234",
        },
        {"error": "The following fields are required and cannot be empty: firstname"},
    )

    check_post(
        "/api/register",
        400,
        {
            "username": "user",
            "firstname": "firstname",
            "lastname": "",
            "email": "email@email.com",
            "password": "1234",
        },
        {"error": "The following fields are required and cannot be empty: lastname"},
    )

    check_post(
        "/api/register",
        400,
        {
            "username": "user",
            "firstname": "firstname",
            "lastname": "lastname",
            "email": "email@email.com",
            "password": "",
        },
        {"error": "The following fields are required and cannot be empty: password"},
    )

    check_post(
        "/api/register",
        400,
        {
            "username": "user",
            "firstname": "firstname",
            "lastname": "lastname",
            "email": "",
            "password": "1234",
        },
        {"error": "The following fields are required and cannot be empty: email"},
    )


def test_login():
    check_login_token(
        "/api/login",
        {"username": "user", "password": "1234"},
    )

    check_post(
        "/api/login",
        401,
        {"username": "user", "password": "bad"},
        {"error": "Incorrect password"},
    )

    check_post(
        "/api/login",
        400,
        {"username": "", "password": "1234"},
        {"error": "The following fields are required and cannot be empty: username"},
    )

    check_post(
        "/api/login",
        400,
        {"username": None, "password": "1234"},
        {"error": "The following fields are required and cannot be empty: username"},
    )

    check_post(
        "/api/login",
        400,
        {"username": "", "password": ""},
        {
            "error": "The following fields are required and cannot be empty: username, password"
        },
    )

    check_post(
        "/api/login",
        401,
        {"username": "no_user", "password": "1234"},
        {"error": "Incorrect username"},
    )

    check_post(
        "/api/login",
        400,
        {"password": "1234"},
        {"error": "The following fields are required and cannot be empty: username"},
    )


def test_update():
    check_get_token(
        "/api/profile",
        200,
        {
            "age": None,
            "bio": None,
            "email": "email@email.com",
            "email_verified": False,
            "fameRating": 0,
            "firstname": "firstname",
            "interests": [],
            "lastname": "lastname",
            "likedBy": [],
            "profile_complete": False,
            "selectedGender": None,
            "sexualPreference": None,
            "urlProfile": "no url",
            "username": "user",
            "visitedBy": [],
        },
    )
    check_put_token(
        "/api/profile",
        400,
        {"email": "b@b.com"},
        {
            "error": "The following fields are required and cannot be empty: firstname, lastname, selectedGender, sexualPreference, bio, age"
        },
    )
    check_put_token(
        "/api/profile",
        200,
        {
            "age": "22",
            "firstname": "Johnny",
            "lastname": "Appleseed",
            "selectedGender": "m",
            "sexualPreference": "e",
            "bio": "I am a very interesting person. I like to do interesting things and go to interesting places. I am looking for someone who is also interesting.",
        },
        {
            "age": 22,
            "bio": "I am a very interesting person. I like to do interesting things and go to interesting places. I am looking for someone who is also interesting.",
            "email": "email@email.com",
            "email_verified": False,
            "fameRating": 0,
            "firstname": "Johnny",
            "interests": [],
            "lastname": "Appleseed",
            "likedBy": [],
            "profile_complete": True,
            "selectedGender": "m",
            "sexualPreference": "e",
            "urlProfile": "no url",
            "username": "user",
            "visitedBy": [],
        },
    )
    check_put_token(
        "/api/profile",
        200,
        {
            "age": 22,
            "firstname": "Johnny",
            "lastname": "Appleseed",
            "selectedGender": "ma",
            "sexualPreference": "e",
            "bio": "I am a very interesting person. I like to do interesting things and go to interesting places. I am looking for someone who is also interesting.",
        },
        {"error": "value too long for type character(1)\n"},
    )
    check_put(
        "/api/profile",
        401,
        {"firstname": "Johnny"},
        {"msg": "Missing Authorization Header"},
    )
    check_get_token(
        "/api/profile",
        200,
        {
            "age": 22,
            "bio": "I am a very interesting person. I like to do interesting things and go to interesting places. I am looking for someone who is also interesting.",
            "email": "email@email.com",
            "email_verified": False,
            "fameRating": 0,
            "firstname": "Johnny",
            "interests": [],
            "lastname": "Appleseed",
            "likedBy": [],
            "profile_complete": True,
            "selectedGender": "m",
            "sexualPreference": "e",
            "urlProfile": "no url",
            "username": "user",
            "visitedBy": [],
        },
    )
    check_get_token(
        "/api/profile/another",
        200,
        {
            "age": 18,
            "bio": "My bio is short. with special a single quote '",
            "connected": False,
            "fameRating": 0,
            "firstname": "Another",
            "gender": "m",
            "interests": [],
            "isLiked": False,
            "isFaked": False,
            "isBlocked": False,
            "lastConnection": 1734914588.912091,
            "lastname": "User",
            "pictures": [],
            "sexualPreference": "e",
            "urlProfile": "no url",
            "username": "another",
        },
    )
    check_get_token(
        "/api/profile/ another",
        401,
        {
            "error": "username not found",
        },
    )
    check_get_token(
        "/api/profile/another'",
        401,
        {
            "error": "username not found",
        },
    )
    check_login_token(
        "/api/login",
        {"username": "another", "password": "5678"},
    )
    check_get_token(
        "/api/profile",
        200,
        {
            "age": 18,
            "bio": "My bio is short. with special a single quote '",
            "email": "another@flask.py",
            "email_verified": False,
            "fameRating": 0,
            "firstname": "Another",
            "interests": [],
            "lastname": "User",
            "likedBy": [],
            "profile_complete": True,
            "selectedGender": "m",
            "sexualPreference": "e",
            "urlProfile": "no url",
            "username": "another",
            "visitedBy": ["user"],
        },
    )


def test_interests():
    check_get_token("/api/interests", 201, {"interests": []})
    check_put_token(
        "/api/interests",
        201,
        {"interests": ["hiking", "technology", "fashion", "nature", "meditation"]},
        {"interests": ["fashion", "hiking", "meditation", "nature", "technology"]},
    )
    check_get_token(
        "/api/interests",
        201,
        {"interests": ["fashion", "hiking", "meditation", "nature", "technology"]},
    )
    check_put_token(
        "/api/interests",
        201,
        {
            "interests": [
                "hiking",
                "technology",
                "fashion",
                "nature",
                "meditation",
            ]
        },
        {"interests": ["fashion", "hiking", "meditation", "nature", "technology"]},
    )
    check_get_token(
        "/api/interests",
        201,
        {"interests": ["fashion", "hiking", "meditation", "nature", "technology"]},
    )
    check_put_token(
        "/api/interests",
        201,
        {"interests": []},
        {"interests": []},
    )
    check_get_token(
        "/api/interests",
        201,
        {"interests": []},
    )


def test_pictures():
    check_get_token_pictures("/api/pictures", 201, {"pictures": 0})
    check_post_token_pictures(
        "/api/pictures",
        200,
        "../frontend/AngularApp/public/dummy-pics/placeholderPic.jpg",
        {"pictures": 1},
    )
    check_post_token_pictures(
        "/api/pictures",
        201,
        [
            "../frontend/AngularApp/public/dummy-pics/placeholderPic.jpg",
            "../frontend/AngularApp/public/dummy-pics/placeholderPic.jpg",
        ],
        {"pictures": 3},
    )
    check_post_token_pictures(
        "/api/pictures",
        401,
        [
            "../frontend/AngularApp/public/dummy-pics/placeholderPic.jpg",
            "../frontend/AngularApp/public/dummy-pics/placeholderPic.jpg",
            "../frontend/AngularApp/public/dummy-pics/placeholderPic.jpg",
        ],
        {"error": "too many pictures"},
    )
    check_post_token_pictures(
        "/api/pictures",
        201,
        [
            "../frontend/AngularApp/public/dummy-pics/placeholderPic.jpg",
            "../frontend/AngularApp/public/dummy-pics/placeholderPic.jpg",
        ],
        {"pictures": 5},
    )
    pictures = check_get_token_pictures("/api/pictures", 201, {"pictures": 5})
    check_put_token_pictures(
        "/api/profile-picture",
        201,
        {
            "selectedPictures": pictures[1],
        },
        {"selectedPicture": 1},
    )
    check_get_token_pictures("/api/profile-picture", 201, {"selectedPicture": 1})
    check_delete_token_body(
        "/api/pictures",
        201,
        {
            "url": pictures,
        },
        {"pictures": []},
    )


def test_email():
    check_put_token(
        "/api/email",
        201,
        {
            "email": "test@python.py",
        },
        {"email": "test@python.py"},
    )
    check_get_token("/api/email", 201, {"email": "test@python.py"})


def test_deleteme():
    check_login_token(
        "/api/login",
        {"username": "user", "password": "1234"},
    )
    check_get_token("/api/deleteme", 200, {"success": "user delete"})
    check_login_token(
        "/api/login",
        {"username": "notcompleted", "password": "notcompleted"},
    )
    check_get_token("/api/deleteme", 200, {"success": "user delete"})
    check_login_token(
        "/api/login",
        {"username": "another", "password": "5678"},
    )
    check_get_token("/api/deleteme", 200, {"success": "user delete"})


def test_reset_password():
    check_post(
        "/api/reset-password",
        201,
        {"username": "user"},
        {"success": "ok"},
    )
    check_post(
        "/api/reset-password",
        201,
        {"username": "thisusernamedoesnotexist"},
        {"success": "ok"},
    )
    check_login_token(
        "/api/login",
        {"username": "another", "password": "5678"},
    )
    check_post(
        "/api/reset-password",
        201,
        {"username": "another"},
        {"success": "ok"},
    )
    url = confirm_get_last_url()
    confirm_token = url.removeprefix("http://localhost:5001" + "/api/reset-password/")
    check_post(
        "/api/reset-password/" + confirm_token,
        201,
        {"password": "1234"},
        {"success": "password reset"},
    )


def test_browsing():
    check_post_token(
        "/api/browsing",
        200,
        {
            "ageGap": 0,
            "fameGap": 0,
            "distance": 0,
            "interests": [],
        },
        [],
    )
    check_post_token(
        "/api/browsing",
        200,
        {
            "ageGap": 31,
            "fameGap": 5,
            "distance": 42,  # update users set (latitude, longitude) = (46.532327, 6.591987) where username = 'user'
            "interests": [],
        },
        [
            {
                "age": 110,
                "fameRating": 4,
                "firstname": "Marquise",
                "gender": "f",
                "interests": [
                    "cats",
                    "fashion",
                    "gaming",
                    "music",
                    "nature",
                    "reading",
                    "tattoos",
                ],
                "lastname": "Kautzer",
                "sexualPreference": "e",
                "urlProfile": "no url",
                "username": "marquise",
            },
            {
                "age": 18,
                "fameRating": 2,
                "firstname": "Camren",
                "gender": "f",
                "interests": [
                    "dogs",
                    "fitness",
                    "meditation",
                    "movies",
                    "nature",
                    "photography",
                    "reading",
                    "tattoos",
                    "yoga",
                ],
                "lastname": "Bechtelar",
                "sexualPreference": "e",
                "urlProfile": "no url",
                "username": "camren",
            },
        ],
    )
    check_post_token(
        "/api/browsing",
        200,
        {
            "ageGap": 20,
            "fameGap": 5,
            "distance": 101,
            "interests": [],
        },
        [
            {
                "age": 18,
                "fameRating": 2,
                "firstname": "Mitchel",
                "gender": "f",
                "interests": [
                    "cats",
                    "gaming",
                    "meditation",
                    "movies",
                    "music",
                    "nature",
                    "photography",
                ],
                "lastname": "Legros",
                "sexualPreference": "e",
                "urlProfile": "no url",
                "username": "mitchel",
            },
            {
                "age": 22,
                "fameRating": 4,
                "firstname": "Abel",
                "gender": "f",
                "interests": [
                    "cooking",
                    "dance",
                    "fashion",
                    "hiking",
                    "movies",
                    "music",
                    "photography",
                    "reading",
                    "tattoos",
                    "technology",
                ],
                "lastname": "Will",
                "sexualPreference": "e",
                "urlProfile": "no url",
                "username": "abel",
            },
            {
                "age": 38,
                "fameRating": 2,
                "firstname": "Antoinette",
                "gender": "f",
                "interests": [
                    "cooking",
                    "dogs",
                    "hiking",
                    "movies",
                    "music",
                    "reading",
                    "tattoos",
                    "travel",
                    "yoga",
                ],
                "lastname": "Krajcik",
                "sexualPreference": "e",
                "urlProfile": "no url",
                "username": "antoinette",
            },
            {
                "age": 18,
                "fameRating": 4,
                "firstname": "Bonnie",
                "gender": "f",
                "interests": [
                    "dogs",
                    "fashion",
                    "fitness",
                    "hiking",
                    "photography",
                    "reading",
                    "tattoos",
                    "yoga",
                ],
                "lastname": "Wuckert",
                "sexualPreference": "e",
                "urlProfile": "no url",
                "username": "bonnie",
            },
            {
                "age": 30,
                "fameRating": 2,
                "firstname": "Antwon",
                "gender": "f",
                "interests": [
                    "cooking",
                    "fashion",
                    "gaming",
                    "meditation",
                    "movies",
                    "nature",
                    "yoga",
                ],
                "lastname": "O'Hara",
                "sexualPreference": "e",
                "urlProfile": "no url",
                "username": "antwon",
            },
            {
                "age": 18,
                "fameRating": 4,
                "firstname": "Josiane",
                "gender": "f",
                "interests": [
                    "cooking",
                    "gaming",
                    "hiking",
                    "movies",
                    "music",
                    "tattoos",
                    "yoga",
                ],
                "lastname": "Fisher",
                "sexualPreference": "e",
                "urlProfile": "no url",
                "username": "josiane",
            },
            {
                "age": 18,
                "fameRating": 0,
                "firstname": "Bethany",
                "gender": "f",
                "interests": [
                    "cats",
                    "cooking",
                    "dance",
                    "dogs",
                    "fashion",
                    "hiking",
                    "meditation",
                    "movies",
                    "music",
                    "nature",
                    "reading",
                    "tattoos",
                ],
                "lastname": "Hintz",
                "sexualPreference": "e",
                "urlProfile": "no url",
                "username": "bethany",
            },
            {
                "age": 18,
                "fameRating": 2,
                "firstname": "Camren",
                "gender": "f",
                "interests": [
                    "dogs",
                    "fitness",
                    "meditation",
                    "movies",
                    "nature",
                    "photography",
                    "reading",
                    "tattoos",
                    "yoga",
                ],
                "lastname": "Bechtelar",
                "sexualPreference": "e",
                "urlProfile": "no url",
                "username": "camren",
            },
        ],
    )
    check_post_token(
        "/api/browsing",
        200,
        {
            "ageGap": 15,
            "fameGap": 3,
            "distance": 101,
            "interests": [],
        },
        [
            {
                "age": 18,
                "fameRating": 2,
                "firstname": "Mitchel",
                "gender": "f",
                "interests": [
                    "cats",
                    "gaming",
                    "meditation",
                    "movies",
                    "music",
                    "nature",
                    "photography",
                ],
                "lastname": "Legros",
                "sexualPreference": "e",
                "urlProfile": "no url",
                "username": "mitchel",
            },
            {
                "age": 30,
                "fameRating": 2,
                "firstname": "Antwon",
                "gender": "f",
                "interests": [
                    "cooking",
                    "fashion",
                    "gaming",
                    "meditation",
                    "movies",
                    "nature",
                    "yoga",
                ],
                "lastname": "O'Hara",
                "sexualPreference": "e",
                "urlProfile": "no url",
                "username": "antwon",
            },
            {
                "age": 18,
                "fameRating": 0,
                "firstname": "Bethany",
                "gender": "f",
                "interests": [
                    "cats",
                    "cooking",
                    "dance",
                    "dogs",
                    "fashion",
                    "hiking",
                    "meditation",
                    "movies",
                    "music",
                    "nature",
                    "reading",
                    "tattoos",
                ],
                "lastname": "Hintz",
                "sexualPreference": "e",
                "urlProfile": "no url",
                "username": "bethany",
            },
            {
                "age": 18,
                "fameRating": 2,
                "firstname": "Camren",
                "gender": "f",
                "interests": [
                    "dogs",
                    "fitness",
                    "meditation",
                    "movies",
                    "nature",
                    "photography",
                    "reading",
                    "tattoos",
                    "yoga",
                ],
                "lastname": "Bechtelar",
                "sexualPreference": "e",
                "urlProfile": "no url",
                "username": "camren",
            },
        ],
    )
    check_post_token(
        "/api/browsing",
        200,
        {
            "ageGap": 31,
            "fameGap": 1,
            "distance": 101,
            "interests": [],
        },
        [
            {
                "age": 82,
                "fameRating": 0,
                "firstname": "Doris",
                "gender": "f",
                "interests": [
                    "cooking",
                    "dance",
                    "fashion",
                    "fitness",
                    "meditation",
                    "music",
                    "photography",
                    "reading",
                    "yoga",
                ],
                "lastname": "Altenwerth",
                "sexualPreference": "e",
                "urlProfile": "no url",
                "username": "doris",
            },
            {
                "age": 60,
                "fameRating": 0,
                "firstname": "Jazmin",
                "gender": "f",
                "interests": [
                    "cooking",
                    "fashion",
                    "hiking",
                    "meditation",
                    "nature",
                    "reading",
                    "technology",
                    "yoga",
                ],
                "lastname": "O'Conner",
                "sexualPreference": "e",
                "urlProfile": "no url",
                "username": "jazmin",
            },
            {
                "age": 58,
                "fameRating": 0,
                "firstname": "Marquis",
                "gender": "f",
                "interests": [
                    "cats",
                    "cooking",
                    "gaming",
                    "hiking",
                    "meditation",
                    "movies",
                    "tattoos",
                    "travel",
                ],
                "lastname": "Waelchi",
                "sexualPreference": "e",
                "urlProfile": "no url",
                "username": "marquis",
            },
            {
                "age": 46,
                "fameRating": 0,
                "firstname": "Philip",
                "gender": "f",
                "interests": [
                    "cooking",
                    "dance",
                    "dogs",
                    "hiking",
                    "meditation",
                    "movies",
                    "nature",
                    "photography",
                    "reading",
                    "technology",
                ],
                "lastname": "Dicki",
                "sexualPreference": "e",
                "urlProfile": "no url",
                "username": "philip",
            },
            {
                "age": 62,
                "fameRating": 0,
                "firstname": "Ardella",
                "gender": "f",
                "interests": [
                    "fitness",
                    "gaming",
                    "hiking",
                    "meditation",
                    "movies",
                    "nature",
                    "photography",
                    "reading",
                    "technology",
                    "travel",
                ],
                "lastname": "Swift",
                "sexualPreference": "e",
                "urlProfile": "no url",
                "username": "ardella",
            },
            {
                "age": 112,
                "fameRating": 0,
                "firstname": "Eve",
                "gender": "f",
                "interests": [
                    "cats",
                    "cooking",
                    "dogs",
                    "gaming",
                    "hiking",
                    "meditation",
                    "music",
                    "nature",
                    "reading",
                    "technology",
                    "yoga",
                ],
                "lastname": "Schowalter",
                "sexualPreference": "e",
                "urlProfile": "no url",
                "username": "eve",
            },
            {
                "age": 68,
                "fameRating": 0,
                "firstname": "Luella",
                "gender": "f",
                "interests": [
                    "dogs",
                    "fashion",
                    "fitness",
                    "gaming",
                    "nature",
                    "reading",
                    "tattoos",
                ],
                "lastname": "Brown",
                "sexualPreference": "e",
                "urlProfile": "no url",
                "username": "luella",
            },
            {
                "age": 98,
                "fameRating": 0,
                "firstname": "Leta",
                "gender": "f",
                "interests": [
                    "cats",
                    "cooking",
                    "fashion",
                    "gaming",
                    "reading",
                    "technology",
                    "travel",
                ],
                "lastname": "Hyatt",
                "sexualPreference": "e",
                "urlProfile": "no url",
                "username": "leta",
            },
            {
                "age": 52,
                "fameRating": 0,
                "firstname": "Glenna",
                "gender": "f",
                "interests": [
                    "cats",
                    "cooking",
                    "movies",
                    "nature",
                    "reading",
                    "tattoos",
                    "technology",
                ],
                "lastname": "Lehner",
                "sexualPreference": "e",
                "urlProfile": "no url",
                "username": "glenna",
            },
            {
                "age": 18,
                "fameRating": 0,
                "firstname": "Bethany",
                "gender": "f",
                "interests": [
                    "cats",
                    "cooking",
                    "dance",
                    "dogs",
                    "fashion",
                    "hiking",
                    "meditation",
                    "movies",
                    "music",
                    "nature",
                    "reading",
                    "tattoos",
                ],
                "lastname": "Hintz",
                "sexualPreference": "e",
                "urlProfile": "no url",
                "username": "bethany",
            },
        ],
    )
    check_post_token(
        "/api/browsing",
        200,
        {
            "ageGap": 31,
            "fameGap": 1,
            "distance": 101,
            "interests": ["fitness", "music", "yoga"],
        },
        [
            {
                "age": 82,
                "fameRating": 0,
                "firstname": "Doris",
                "gender": "f",
                "interests": [
                    "cooking",
                    "dance",
                    "fashion",
                    "fitness",
                    "meditation",
                    "music",
                    "photography",
                    "reading",
                    "yoga",
                ],
                "lastname": "Altenwerth",
                "sexualPreference": "e",
                "urlProfile": "no url",
                "username": "doris",
            }
        ],
    )
    check_post_token(
        "/api/browsing",
        200,
        {
            "ageGap": 31,
            "fameGap": 5,
            "distance": 101,
            "interests": ["travel", "reading"],
        },
        [
            {
                "age": 38,
                "fameRating": 2,
                "firstname": "Antoinette",
                "gender": "f",
                "interests": [
                    "cooking",
                    "dogs",
                    "hiking",
                    "movies",
                    "music",
                    "reading",
                    "tattoos",
                    "travel",
                    "yoga",
                ],
                "lastname": "Krajcik",
                "sexualPreference": "e",
                "urlProfile": "no url",
                "username": "antoinette",
            },
            {
                "age": 62,
                "fameRating": 0,
                "firstname": "Ardella",
                "gender": "f",
                "interests": [
                    "fitness",
                    "gaming",
                    "hiking",
                    "meditation",
                    "movies",
                    "nature",
                    "photography",
                    "reading",
                    "technology",
                    "travel",
                ],
                "lastname": "Swift",
                "sexualPreference": "e",
                "urlProfile": "no url",
                "username": "ardella",
            },
            {
                "age": 98,
                "fameRating": 0,
                "firstname": "Leta",
                "gender": "f",
                "interests": [
                    "cats",
                    "cooking",
                    "fashion",
                    "gaming",
                    "reading",
                    "technology",
                    "travel",
                ],
                "lastname": "Hyatt",
                "sexualPreference": "e",
                "urlProfile": "no url",
                "username": "leta",
            },
        ],
    )
    check_post(
        "/api/register",
        200,
        {
            "username": "notcompleted",
            "firstname": "Not",
            "lastname": "Completed",
            "email": "notcompleted@flask.py",
            "password": "notcompleted",
        },
        {"success": "User notcompleted was successfully added"},
    )
    check_login_token(
        "/api/login",
        {"username": "notcompleted", "password": "notcompleted"},
    )
    check_post_token(
        "/api/browsing",
        400,
        {
            "ageGap": 31,
            "fameGap": 5,
            "distance": 101,
            "interests": ["travel", "reading"],
        },
        {"error": "profile not completed"},
    )


def test_like_user():
    check_login_token(
        "/api/login",
        {"username": "user", "password": "1234"},
    )
    check_get_token(
        "/api/like-user",
        201,
        {
            "likers": [],
        },
    )
    check_post_token(
        "/api/like-user",
        201,
        {
            "like": "another",
        },
        {
            "isLiked": True,
        },
    )
    check_post_token(
        "/api/like-user",
        201,
        {
            "like": "daphnee",
        },
        {
            "isLiked": True,
        },
    )
    check_login_token(
        "/api/login",
        {"username": "another", "password": "5678"},
    )
    check_get_token(
        "/api/like-user",
        201,
        {
            "likers": ["user"],
        },
    )
    check_post_token(
        "/api/like-user",
        201,
        {
            "like": "edythe",
        },
        {
            "isLiked": True,
        },
    )
    check_post_token(
        "/api/like-user",
        201,
        {
            "like": "user",
        },
        {
            "isLiked": True,
        },
    )
    check_get_token(
        "/api/match",
        201,
        ["user"],
    )
    check_post_token(
        "/api/like-user",
        201,
        {
            "unlike": "user",
        },
        {
            "isLiked": False,
        },
    )
    check_get_token(
        "/api/match",
        201,
        [],
    )
    check_post_token(
        "/api/like-user",
        201,
        {
            "like": "user",
        },
        {
            "isLiked": True,
        },
    )

    check_login_token(
        "/api/login",
        {"username": "user", "password": "1234"},
    )
    check_post_token(
        "/api/like-user",
        201,
        {
            "unlike": "another",
        },
        {
            "isLiked": False,
        },
    )
    check_login_token(
        "/api/login",
        {"username": "another", "password": "5678"},
    )
    check_get_token(
        "/api/like-user",
        201,
        {
            "likers": [],
        },
    )
    check_post_token(
        "/api/like-user",
        201,
        {
            "unlike": "user",
        },
        {
            "isLiked": False,
        },
    )
    check_login_token(
        "/api/login",
        {"username": "user", "password": "1234"},
    )
    check_get_token(
        "/api/like-user",
        201,
        {
            "likers": [],
        },
    )
    check_get_token(
        "/api/profile",
        200,
        {
            "age": 22,
            "bio": "I am a very interesting person. I like to do interesting things and go to interesting places. I am looking for someone who is also interesting.",
            "email": "email@email.com",
            "email_verified": False,
            "fameRating": 1,
            "firstname": "Johnny",
            "interests": [],
            "lastname": "Appleseed",
            "likedBy": [],
            "profile_complete": True,
            "selectedGender": "m",
            "sexualPreference": "e",
            "urlProfile": "http://localhost:5001/api/images/avatar.png",
            "username": "user",
            "visitedBy": [],
        },
    )


def _test_delete_notification():
    check_login_token(
        "/api/login",
        {"username": "user", "password": "1234"},
    )
    notifications = check_get_token(
        "/api/notification",
        201,
        [
            {
                "content": "another like you",
                "id": 389,
                "timestamp": 1734812518.117288,
                "title": "like",
            },
            {
                "content": "another unlike you",
                "id": 390,
                "timestamp": 1734812518.195932,
                "title": "unlike",
            },
            {
                "content": "another like you",
                "id": 391,
                "timestamp": 1734812518.264354,
                "title": "like",
            },
            {
                "content": "another unlike you",
                "id": 393,
                "timestamp": 1734812518.729724,
                "title": "unlike",
            },
            {
                "content": "message from another",
                "id": 395,
                "timestamp": 1734812519.500513,
                "title": "chat",
            },
            {
                "content": "another like you",
                "id": 396,
                "timestamp": 1734812519.913834,
                "title": "like",
            },
            {
                "content": "another viewed your profile",
                "id": 397,
                "timestamp": 1734812520.030613,
                "title": "visit",
            },
        ],
    )
    for notification in notifications:
        check_delete_token(
            f"/api/notification/{notification['id']}",
            201,
            {
                "delete": notification["id"],
            },
        )


def test_notification():
    check_login_token(
        "/api/login",
        {"username": "another", "password": "5678"},
    )
    check_post_token(
        "/api/like-user",
        201,
        {
            "like": "user",
        },
        {
            "isLiked": True,
        },
    )
    check_get_token(
        "/api/profile/user",
        200,
        {
            "age": 22,
            "bio": "I am a very interesting person. I like to do interesting things and go to interesting places. I am looking for someone who is also interesting.",
            "connected": False,
            "fameRating": 0,
            "firstname": "Johnny",
            "gender": "m",
            "interests": [],
            "isLiked": True,
            "isFaked": False,
            "isBlocked": False,
            "lastConnection": 1735056819.039922,
            "lastname": "Appleseed",
            "pictures": [],
            "sexualPreference": "e",
            "urlProfile": "no url",
            "username": "user",
        },
    )
    _test_delete_notification()


def test_position():
    check_get_token(
        "/api/position",
        201,
        {"latitude": None, "longitude": None},
    )
    check_post_token(
        "/api/position",
        201,
        {"latitude": 46.532327, "longitude": 6.591987},
        {"latitude": 46.532327, "longitude": 6.591987},
    )
    check_post_token(
        "/api/position",
        422,
        {"latitude": "no a float", "longitude": 999},
        {"error": "bad input"},
    )
    check_get_token(
        "/api/position",
        201,
        {"latitude": 46.532327, "longitude": 6.591987},
    )


def test_chat():
    check_login_token(
        "/api/login",
        {"username": "user", "password": "1234"},
    )
    check_get_token(
        "/api/chat/another",
        200,
        [],
    )
    check_post_token(
        "/api/chat",
        201,
        {
            "to": "another",
            "message": "Hi another",
        },
        {"message": "Hi another", "sender": "user", "timestamp": 1734042686.615507},
    )
    check_get_token(
        "/api/chat/another'",
        401,
        {"error": "username not found"},
    )
    check_get_token(
        "/api/chat/another",
        200,
        [{"message": "Hi another", "sender": "user", "timestamp": 1734008116.142995}],
    )
    check_login_token(
        "/api/login",
        {"username": "another", "password": "5678"},
    )
    check_get_token(
        "/api/chat/user",
        200,
        [{"message": "Hi another", "sender": "user", "timestamp": 1734008187.052514}],
    )
    check_post_token(
        "/api/chat",
        201,
        {
            "to": "user",
            "message": "Hi user",
        },
        {"message": "Hi user", "sender": "another", "timestamp": 1734042655.928707},
    )
    check_login_token(
        "/api/login",
        {"username": "user", "password": "1234"},
    )
    check_get_token(
        "/api/chat/another",
        200,
        [
            {"message": "Hi another", "sender": "user", "timestamp": 1734008187.052514},
            {"message": "Hi user", "sender": "another", "timestamp": 1734008187.249586},
        ],
    )


def test_fake():
    check_post_token(
        "/api/fake",
        201,
        {
            "fake": "another",
        },
        {"isFaked": True},
    )
    check_get_token(
        "/api/profile/another",
        200,
        {
            "age": 18,
            "bio": "My bio is short. with special a single quote '",
            "connected": False,
            "fameRating": 0,
            "firstname": "Another",
            "gender": "m",
            "interests": [],
            "isLiked": False,
            "isFaked": True,
            "isBlocked": False,
            "lastConnection": 1734914588.912091,
            "lastname": "User",
            "pictures": [],
            "sexualPreference": "e",
            "urlProfile": "no url",
            "username": "another",
        },
    )
    check_post_token(
        "/api/fake",
        201,
        {
            "unfake": "another",
        },
        {"isFaked": False},
    )
    check_get_token(
        "/api/profile/another",
        200,
        {
            "age": 18,
            "bio": "My bio is short. with special a single quote '",
            "connected": False,
            "fameRating": 0,
            "firstname": "Another",
            "gender": "m",
            "interests": [],
            "isLiked": False,
            "isFaked": False,
            "isBlocked": False,
            "lastConnection": 1734914588.912091,
            "lastname": "User",
            "pictures": [],
            "sexualPreference": "e",
            "urlProfile": "no url",
            "username": "another",
        },
    )


def test_block():
    check_post_token(
        "/api/block",
        201,
        {
            "block": "another",
        },
        {"isBlocked": True},
    )
    check_post_token(
        "/api/block",
        201,
        {
            "unblock": "another",
        },
        {"isBlocked": False},
    )


def test_confirm():
    check_login_token(
        "/api/login",
        {"username": "another", "password": "5678"},
    )
    check_get_token(
        "/api/confirm",
        201,
        {
            "success": "mail sent",
        },
    )
    url = confirm_get_last_url()
    confirm_token = url.removeprefix("http://localhost:5001" + "/api/confirm/")
    check_get_token(
        "/api/confirm/" + confirm_token,
        201,
        {
            "success": "ok",
        },
    )
    check_get_token(
        "/api/profile",
        200,
        {
            "age": 18,
            "bio": "My bio is short. with special a single quote '",
            "email": "test@python.py",
            "email_verified": True,
            "fameRating": 0,
            "firstname": "Another",
            "interests": [],
            "lastname": "User",
            "likedBy": [],
            "profile_complete": True,
            "selectedGender": "m",
            "sexualPreference": "e",
            "urlProfile": "no url",
            "username": "another",
            "visitedBy": ["user"],
        },
    )
    check_get_token(
        "/api/confirm/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.eyJpZF91c2VyIjoyNjUsImVtYWlsIjoiZW1haWwifQ.wcMsNi2aafLInc_8NcUjh0Ldzq5zKm7CvwAi4RpD1rtm91hFQVfLEl09txwJT0u85poWe-TJjbIopMchuJQhhQ",
        401,
        {
            "error": "bad token",
        },
    )
    check_get_token(
        "/api/confirm/dummy",
        401,
        {
            "error": "bad token",
        },
    )


def main():
    test_register()
    test_create_another_user()
    test_login()
    test_update()
    test_interests()
    test_pictures()
    test_email()
    test_position()
    test_browsing()
    test_like_user()
    test_chat()
    test_notification()
    test_fake()
    test_block()
    test_confirm()
    test_reset_password()
    test_deleteme()


if __name__ == "__main__":
    main()
