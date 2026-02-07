from services.moodle_client import MoodleClient

client = MoodleClient()

def get_all_users():
    result = client.call(
        "core_user_get_users",
        {
            "criteria[0][key]": "email",
            "criteria[0][value]": "%"
        }
    )
    return result.get("users", [])


def get_user_by_email(email: str):
    result = client.call(
        "core_user_get_users",
        {
            "criteria[0][key]": "email",
            "criteria[0][value]": email
        }
    )
    users = result.get("users", [])
    return users[0] if users else None

def suspend_user(user_id: int):
    return client.call(
        "core_user_update_users",
        {
            "users[0][id]": user_id,
            "users[0][suspended]": 1
        }
    )

def unsuspend_user(user_id: int):
    return client.call(
        "core_user_update_users",
        {
            "users[0][id]": user_id,
            "users[0][suspended]": 0
        }
    )
def extract_phone(user: dict):
    """
    Returns phone number from standard or custom fields
    """
    # 1️⃣ Standard Moodle fields
    if user.get("phone1"):
        return user["phone1"]
    if user.get("phone2"):
        return user["phone2"]

    # 2️⃣ Custom profile fields (very common)
    for field in user.get("customfields", []):
        if field.get("shortname") in ("mobile", "phone", "mobilenumber","mobilephone"):
            return field.get("value")

    return None


def get_user_by_id(user_id: int):
    users = client.call(
        "core_user_get_users_by_field",
        {
            "field": "id",
            "values[0]": user_id
        }
    )
    return users[0] if users else {}


def get_user_courses(user_id: int):
    """
    Returns courses user is enrolled in,
    with last access time per course
    """
    return client.call(
        "core_enrol_get_users_courses",
        {
            "userid": user_id
        }
    )