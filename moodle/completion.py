from services.moodle_client import MoodleClient
from datetime import datetime


client = MoodleClient()

def get_course_completion(course_id: int, user_id: int):
    return client.call(
        "core_completion_get_course_completion_status",
        {
            "courseid": course_id,
            "userid": user_id
        }
    )



def get_activity_completion(user_id: int, course_id: int):
    """
    Returns completion status for all activities in a course for a user
    """
    response = client.call(
        "core_completion_get_activities_completion_status",
        {
            "userid": user_id,
            "courseid": course_id
        }
    )
    return response.get("statuses", [])
