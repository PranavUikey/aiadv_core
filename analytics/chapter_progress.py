from moodle.courses import get_course_contents
from moodle.completion import get_activity_completion




def is_each_chapter_started(user_id: int, course_id: int):
    """
    Returns chapter-wise progress:
    at least one completed topic per chapter
    """
    sections = get_course_contents(course_id)
    activity_status = get_activity_completion(user_id, course_id)

    # Map activity id → completion state
    completion_map = {
        a["cmid"]: a["state"]
        for a in activity_status
    }

    chapter_report = []

    for section in sections:
        section_name = section.get("name", "Unnamed Section")
        modules = section.get("modules", [])

        completed_in_section = False

        for module in modules:
            cmid = module.get("id")
            if completion_map.get(cmid) == 1:  # 1 = completed
                completed_in_section = True
                break

        chapter_report.append({
            "chapter": section_name,
            "has_completed_topic": completed_in_section
        })

    return chapter_report



def get_remaining_chapters(user_id: int, course_id: int):
    """
    Returns remaining chapters (sections) for a user in a course
    """

    report = is_each_chapter_started(user_id, course_id)

    chapters = report["chapter"]


    remaining = [
        c["chapter"]
        for c in chapters
        if not c["has_completed_topic"]
    ]

    return {
        "total_chapters": len(chapters),
        "completed_chapters": len(chapters) - len(remaining),
        "remaining_chapters_count": len(remaining),
        "remaining_chapters": remaining
    }
