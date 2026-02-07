from datetime import datetime, timedelta
from moodle.users import get_all_users, extract_phone, get_user_courses
from analytics.utils import get_last_accessed_course


SECONDS_IN_DAY = 86400

def get_inactive_students_with_details(days: int):
    now = datetime.utcnow()
    cutoff = int((now - timedelta(days=days)).timestamp())

    inactive_students = []

    users = get_all_users()

    for user in users:
        # Skip guest/system
        if user.get("id") in (1,) or user.get("suspended"):
            continue

        lastaccess = user.get("lastaccess", 0)

        if lastaccess == 0 or lastaccess < cutoff:
            inactive_days = (
                "Never logged in"
                if lastaccess == 0
                else int((now.timestamp() - lastaccess) / SECONDS_IN_DAY)
            )

            courses = get_user_courses(user["id"])
            last_course = get_last_accessed_course(courses)

            inactive_students.append({
                "id": user["id"],
                "name": user["fullname"],
                "email": user["email"],
                "phone": extract_phone(user),
                "inactive_days": inactive_days,
                "current_courses": [c["fullname"] for c in courses],
                "last_accessed_course": last_course
            })

    return inactive_students




def get_recently_inactive_students(days: int = 7):
    """
    Returns students who became inactive in the last `days` window
    (example: 7–14 days inactive, not more than that).
    """
    now = datetime.utcnow()

    upper_cutoff = int((now - timedelta(days=days)).timestamp())
    lower_cutoff = int((now - timedelta(days=days * 2)).timestamp())

    results = []

    users = get_all_users()

    for user in users:
        # Skip guest/system users
        if user.get("id") == 1 or user.get("suspended"):
            continue

        lastaccess = user.get("lastaccess", 0)

        # Skip users who never logged in
        if lastaccess == 0:
            continue

        # ✅ Key condition: inactive ONLY in last 7 days window
        if lower_cutoff <= lastaccess < upper_cutoff:
            inactive_days = int((now.timestamp() - lastaccess) / SECONDS_IN_DAY)

            results.append({
                "id": user["id"],
                "name": user["fullname"],
                "email": user["email"],
                "inactive_days": inactive_days,
                "last_access": datetime.fromtimestamp(
                    lastaccess
                ).strftime("%Y-%m-%d %H:%M:%S")
            })

    return results

