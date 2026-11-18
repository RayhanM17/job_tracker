import json

from matching import match_job, parse_skills, rank_jobs


def test_parse_skills_dedupes_and_trims():
    assert parse_skills(" Python, sql ,python,, Flask") == ["Python", "sql", "Flask"]


def test_full_and_partial_match():
    assert match_job(["python", "sql", "flask"], '["Python","SQL","Flask"]')["percent"] == 100
    r = match_job(["Python", "SQL"], json.dumps(["Python", "SQL", "Tableau"]))
    assert r["percent"] == 67 and r["missing"] == ["Tableau"]


def test_rank_orders_and_drops_zero_matches():
    jobs = [
        {"job_title": "B", "requirements": '["Python","SQL","Tableau"]'},
        {"job_title": "A", "requirements": '["Python","SQL"]'},
        {"job_title": "C", "requirements": '["Go"]'},
    ]
    assert [j["job_title"] for j in rank_jobs(["Python", "SQL"], jobs)] == ["A", "B"]


def test_job_without_requirements():
    assert match_job(["x"], None)["percent"] == 0
