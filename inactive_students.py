from analytics.inactivity import get_recently_inactive_students
from moodle.users import get_user_courses
from analytics.chapter_progress import is_each_chapter_started
from datetime import datetime



def get_inactive_students_mail_data(days=7):
    """
    Returns ONE dictionary per user with multiple courses inside
    """

    students = get_recently_inactive_students(days=days)

    users_map = {}  

    for s in students:
        user_id = s["id"]
        full_name = s["name"]
        email = s["email"]
        first_name = full_name.split()[0]

        # Initialize user once
        if user_id not in users_map:
            users_map[user_id] = {
                "user": {
                    "id": user_id,
                    "first_name": first_name,
                    "full_name": full_name,
                    "email": email,
                },
                "courses": []
            }

        try:
            courses = get_user_courses(user_id)
        except Exception:
            continue

        for c in courses:
            progress = c.get("progress", 0)

            # Only target < 90% completed courses
            if progress is None or ((progress >= 90) and (progress != 100)):
                continue

            try:
                report = is_each_chapter_started(user_id, c["id"])
            except Exception:
                continue

            completed_chapters = sum(
                1 for ch in report if ch["has_completed_topic"]
            )
            total_chapters = len(report)

            remaining_chapters = [
                ch["chapter"] for ch in report
                if not ch["has_completed_topic"]
            ]

            timeaccess = c.get("timeaccess", 0)
            last_course_access = (
                datetime.fromtimestamp(timeaccess).strftime("%Y-%m-%d %H:%M:%S")
                if timeaccess and timeaccess > 0
                else "Never accessed"
            )

            users_map[user_id]["courses"].append({
                "course": {
                    "id": c["id"],
                    "name": c["fullname"],
                    "progress_percent": progress,
                    "last_course_access": last_course_access,
                    "resume_link": f"https://course.aiadventures.in/course/view.php?id={c['id']}"
                },
                "progress": {
                    "completed_chapters": completed_chapters,
                    "total_chapters": total_chapters,
                    "remaining_chapters_count": len(remaining_chapters),
                    "completion_percentage": round(progress, 2)
                },
                "remaining_chapters": remaining_chapters
            })


    return list(users_map.values())

