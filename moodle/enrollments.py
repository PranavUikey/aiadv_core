from services.moodle_client import MoodleClient

client = MoodleClient()

STUDENT_ROLE_ID = 5  # Moodle default

def enroll_user(course_id: int, user_id: int):
    return client.call(
        "enrol_manual_enrol_users",
        {
            "enrolments[0][roleid]": STUDENT_ROLE_ID,
            "enrolments[0][userid]": user_id,
            "enrolments[0][courseid]": course_id
        }
    )

def unenroll_user(course_id: int, user_id: int):
    return client.call(
        "enrol_manual_unenrol_users",
        {
            "enrolments[0][userid]": user_id,
            "enrolments[0][courseid]": course_id
        }
    )
