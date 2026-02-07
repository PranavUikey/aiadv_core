from datetime import datetime

def get_last_accessed_course(courses: list):
    accessed = [c for c in courses if c.get("timeaccess", 0) > 0]

    if not accessed:
        return None

    last_course = max(accessed, key=lambda c: c["timeaccess"])

    return {
        "course_id": last_course["id"],
        "course_name": last_course["fullname"],
        "last_access": datetime.fromtimestamp(
            last_course["timeaccess"]
        ).strftime("%Y-%m-%d %H:%M:%S")
    }
