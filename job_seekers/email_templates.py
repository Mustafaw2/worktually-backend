def get_job_application_email_subject():
    return "New Job Application"


def get_job_application_email_body(organization, job_post, job_seeker, job_application):
    return f"""
        Dear {organization.get("name", "Organization")},

        A new job application has been submitted for the position of {job_post.get("job_title_id", "N/A")}.

        Job Seeker: {job_seeker.first_name} {job_seeker.last_name}
        Job Profile: {job_application.job_profile}
        Source: {job_application.source}

        Best regards,
        Your Recruitment Team
    """