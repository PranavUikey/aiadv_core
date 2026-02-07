def format_email(template: str, user_data: dict):
    courses_block = ""
    resume_links = ""

    for course in user_data["courses"]:
        c = course["course"]
        p = course["progress"]
        remaining = course["remaining_chapters"]

        courses_block += (
            f"📘 Course: {c['name']}\n"
            f"📊 Progress: {p['completion_percentage']}% completed\n"
            f"📍 Chapters remaining: {p['remaining_chapters_count']}\n"
        )

        if remaining:
            courses_block += "Remaining chapters:\n"
            for ch in remaining:
                courses_block += f"• {ch}\n"

        courses_block += "\n" + "-" * 40 + "\n\n"

        resume_links += f"• {c['name']} → {c['resume_link']}\n"

    email_body = template
    email_body = email_body.replace("{{first_name}}", user_data["user"]["first_name"])
    email_body = email_body.replace("{{courses_block}}", courses_block.strip())
    email_body = email_body.replace("{{resume_links_block}}", resume_links.strip())

    return email_body
