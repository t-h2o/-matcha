"""Flask, psycopg2, os.environ, contextmanager"""

from psycopg2.errors import UndefinedTable

from matcha.db.utils import (
    db_query,
    db_fetchone,
)


def db_get_id_where_username(username):
    return db_fetchone("SELECT id FROM users WHERE username = %s", (username,))


def db_get_username_where_id(id_user: int) -> str:
    return db_fetchone("SELECT username FROM users WHERE id = %s", (id_user,))[0]


def db_get_email_where_id(id_user: int) -> str:
    return db_fetchone("SELECT email FROM users WHERE id = %s", (id_user,))[0]


def db_get_email_data_where_username(username: str):
    return db_fetchone(
        "SELECT email, email_verified FROM users WHERE username = %s", (username,)
    )


def db_get_id_password_where_username(username):
    return db_fetchone("SELECT id,password FROM users WHERE username = %s", (username,))


def db_update_password(username: str, password: str):
    query = """
    UPDATE users
    SET
    password = %S
    WHERE
    username = %s
    ;
    """

    error_msg = db_query(
        query,
        (
            password,
            username,
        ),
    )

    if error_msg:
        return error_msg


def db_confirm_email(id_user: int, email: str):
    query = """
    UPDATE users
    SET email_verified = TRUE
    WHERE
    id = %s
    AND
    email = %s
    ;
    """

    error_msg = db_query(
        query,
        (
            id_user,
            email,
        ),
    )

    if error_msg:
        return error_msg


def db_set_user_email(id_user, email):
    error_msg = db_query(
        "UPDATE users SET email = %s where id = %s",
        (
            email,
            id_user,
        ),
    )

    if error_msg:
        return error_msg


def db_get_user_email(id_user):
    return db_fetchone(
        "SELECT email FROM users where id = %s",
        (id_user,),
    )[0]


def db_is_profile_completed(id_user: int):
    return db_fetchone(
        "SELECT profile_complete FROM users where id = %s",
        (id_user,),
    )[0]


def db_set_user_profile_data(
    firstname, lastname, selectedGender, sexualPreference, bio, age, id_user
):
    error_msg = db_query(
        "UPDATE users SET (firstname, lastname, gender, sexual_orientation, bio, age) = (%s, %s, %s, %s, %s, %s) where id = %s",
        (
            firstname,
            lastname,
            selectedGender,
            sexualPreference,
            bio,
            age,
            id_user,
        ),
    )

    if error_msg:
        return error_msg


def db_get_iduser_per_username(username):
    return db_fetchone(
        "SELECT id FROM users WHERE username = %s",
        (username,),
    )


def db_get_user_per_id(id_user):
    return db_fetchone(
        "SELECT username, email, firstname, lastname, gender, sexual_orientation, bio, age, email_verified, profile_complete, fame_rating, latitude, longitude FROM users WHERE id = %s",
        (id_user,),
    )


def db_get_user_per_username(username):
    return db_fetchone(
        "SELECT id, username, firstname, lastname, gender, sexual_orientation, bio, age, fame_rating FROM users WHERE username = %s",
        (username,),
    )


def db_delete_user(id_user):
    error_msg = db_query("DELETE from users where id = (%s);", (id_user,))

    if error_msg:
        return error_msg, 401

    return {"success": "user delete"}, 200


def db_update_by_one_fame_rating(id_user):
    query = """
    UPDATE users
    SET fame_rating
    = cast(profile_complete as int)
    + (select count (*) from user_likes where liked_id = %s)
    + cast(((select count (*) from user_likes where liked_id = %s) > 10) as int)
    WHERE id = %s;
    """

    return db_query(
        query,
        (
            id_user,
            id_user,
            id_user,
        ),
    )
