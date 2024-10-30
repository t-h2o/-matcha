from uuid import uuid4


def check_request_json(content_type, json, required_fields):
    if content_type != "application/json":
        return {"error": "Content-Type not supported!"}, 415

    missing_fields = [
        field for field in required_fields if field not in json or not json[field]
    ]

    if missing_fields:
        return {
            "error": f"The following fields are required and cannot be empty: {', '.join(missing_fields)}"
        }, 400

    return None


def make_unique(string):
    ident = uuid4().__str__()
    return f"{ident}-{string}"
