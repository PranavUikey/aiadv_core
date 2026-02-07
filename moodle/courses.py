from services.moodle_client import MoodleClient

client = MoodleClient()

def get_all_courses():
    return client.call("core_course_get_courses")

def get_course_contents(course_id: int):
    return client.call(
        "core_course_get_contents",
        {"courseid": course_id}
    )

def get_course_by_id(course_id: int):
    courses = client.call(
        "core_course_get_courses",
        {"options[ids][0]": course_id}
    )
    return courses[0] if courses else {}