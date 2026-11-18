"""Skill matching: pure functions, no database or Flask imports."""
import json


def parse_skills(text):
    """'Python, sql ,Flask' -> ['Python', 'sql', 'Flask'] (de-duplicated, case-insensitive)."""
    seen, out = set(), []
    for s in (text or "").split(","):
        s = s.strip()
        if s and s.lower() not in seen:
            seen.add(s.lower())
            out.append(s)
    return out


def match_job(user_skills, requirements):
    """Compare user skills to a job's required skills. Returns percent, matched and missing lists."""
    reqs = json.loads(requirements) if isinstance(requirements, (str, bytes)) else (requirements or [])
    have = {s.lower() for s in user_skills}
    matched = [r for r in reqs if r.lower() in have]
    missing = [r for r in reqs if r.lower() not in have]
    pct = round(100 * len(matched) / len(reqs)) if reqs else 0
    return {"percent": pct, "matched": matched, "missing": missing, "total": len(reqs)}


def rank_jobs(user_skills, jobs):
    """Attach match info to each job dict and sort best-first; jobs with no matches are dropped."""
    ranked = [{**j, **match_job(user_skills, j["requirements"])} for j in jobs]
    ranked = [j for j in ranked if j["matched"]]
    return sorted(ranked, key=lambda j: (-j["percent"], -len(j["matched"]), j["job_title"]))
