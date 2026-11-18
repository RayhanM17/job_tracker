"""Job Application Tracker - Flask entry point."""
from flask import Flask, render_template, request

import database
import matching
from crud import bp as crud_bp
from resources import RESOURCES, STATUSES

app = Flask(__name__)
app.secret_key = "dev-only-change-me"
app.register_blueprint(crud_bp)


@app.context_processor
def nav():
    return {"nav_items": [(k, r["title"]) for k, r in RESOURCES.items()]}


@app.template_filter("pretty")
def pretty(value):
    """Render JSON lists as 'a, b'; booleans as Yes/No; None as a dash."""
    if value is None or value == "":
        return "—"
    if isinstance(value, (bytes, str)) and str(value).startswith("["):
        import json
        return ", ".join(json.loads(value))
    return value


@app.route("/")
def dashboard():
    counts = {k: database.query(f"SELECT COUNT(*) n FROM {r['table']}", one=True)["n"] for k, r in RESOURCES.items()}
    by_status = {s: 0 for s in STATUSES}
    for row in database.query("SELECT status, COUNT(*) n FROM applications GROUP BY status"):
        by_status[row["status"]] = row["n"]
    total = counts["applications"]
    active = sum(by_status[s] for s in ("Applied", "Screening", "Interview"))
    salary = database.query("SELECT ROUND(AVG((salary_min + salary_max) / 2)) avg FROM jobs "
                            "WHERE salary_min IS NOT NULL AND salary_max IS NOT NULL", one=True)["avg"]
    recent = database.query(RESOURCES["applications"]["list_sql"] + " LIMIT 5")
    return render_template("dashboard.html", counts=counts, by_status=by_status, total=total,
                           active=active, salary=salary, recent=recent)


@app.route("/job-match", methods=["GET", "POST"])
def job_match():
    skills_text = request.form.get("skills", "")
    skills = matching.parse_skills(skills_text)
    results = None
    if skills:
        jobs = database.query("SELECT j.*, c.company_name FROM jobs j JOIN companies c USING (company_id)")
        results = matching.rank_jobs(skills, jobs)
    return render_template("job_match.html", skills_text=skills_text, skills=skills, results=results)


if __name__ == "__main__":
    app.run(debug=True)
