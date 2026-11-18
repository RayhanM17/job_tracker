"""Declarative definitions of the four tables. The generic CRUD blueprint is driven by these."""

STATUSES = ["Applied", "Screening", "Interview", "Offer", "Rejected", "Withdrawn"]
JOB_TYPES = ["Full-time", "Part-time", "Contract", "Internship"]


def F(name, label, kind="text", required=False, **extra):
    """Field spec. kind: text|textarea|int|date|enum|fk|bool|list|json"""
    return {"name": name, "label": label, "kind": kind, "required": required, **extra}


COMPANY_FK = F("company_id", "Company", "fk", True, fk="companies")
JOB_FK = F("job_id", "Job", "fk", True, fk="jobs")

RESOURCES = {
    "companies": {
        "title": "Companies", "singular": "Company", "table": "companies", "pk": "company_id",
        "label_sql": "company_name",
        "list_sql": "SELECT * FROM companies ORDER BY company_name",
        "columns": ["company_name", "industry", "city", "state", "website"],
        "fields": [
            F("company_name", "Name", required=True, max=100),
            F("industry", "Industry", max=50),
            F("website", "Website", max=200),
            F("city", "City", max=50),
            F("state", "State", max=50),
            F("notes", "Notes", "textarea"),
        ],
    },
    "jobs": {
        "title": "Jobs", "singular": "Job", "table": "jobs", "pk": "job_id",
        "label_sql": "CONCAT(job_title, ' @ ', (SELECT company_name FROM companies c WHERE c.company_id = jobs.company_id))",
        "list_sql": "SELECT j.*, c.company_name FROM jobs j JOIN companies c USING (company_id) ORDER BY j.date_posted DESC",
        "columns": ["job_title", "company_name", "job_type", "salary_min", "salary_max", "date_posted", "requirements"],
        "fields": [
            COMPANY_FK,
            F("job_title", "Title", required=True, max=100),
            F("job_type", "Type", "enum", options=JOB_TYPES),
            F("salary_min", "Salary min", "int"),
            F("salary_max", "Salary max", "int"),
            F("job_url", "Posting URL", max=300),
            F("date_posted", "Date posted", "date"),
            F("requirements", "Required skills (comma-separated)", "list"),
        ],
    },
    "applications": {
        "title": "Applications", "singular": "Application", "table": "applications", "pk": "application_id",
        "label_sql": "CONCAT('Application #', application_id)",
        "list_sql": ("SELECT a.*, j.job_title, c.company_name FROM applications a "
                     "JOIN jobs j USING (job_id) JOIN companies c USING (company_id) ORDER BY a.application_date DESC"),
        "columns": ["job_title", "company_name", "application_date", "status", "resume_version", "cover_letter_sent"],
        "fields": [
            JOB_FK,
            F("application_date", "Date applied", "date", True),
            F("status", "Status", "enum", options=STATUSES),
            F("resume_version", "Resume version", max=50),
            F("cover_letter_sent", "Cover letter sent", "bool"),
            F("interview_data", "Interview data (JSON object)", "json"),
        ],
    },
    "contacts": {
        "title": "Contacts", "singular": "Contact", "table": "contacts", "pk": "contact_id",
        "label_sql": "contact_name",
        "list_sql": "SELECT ct.*, c.company_name FROM contacts ct JOIN companies c USING (company_id) ORDER BY ct.contact_name",
        "columns": ["contact_name", "title", "company_name", "email", "phone"],
        "fields": [
            COMPANY_FK,
            F("contact_name", "Name", required=True, max=100),
            F("title", "Title", max=100),
            F("email", "Email", max=100),
            F("phone", "Phone", max=20),
            F("linkedin_url", "LinkedIn URL", max=200),
            F("notes", "Notes", "textarea"),
        ],
    },
}
