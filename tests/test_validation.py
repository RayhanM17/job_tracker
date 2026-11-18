from resources import RESOURCES
from validation import validate


def test_required_and_types():
    _, errors = validate(RESOURCES["applications"], {"job_id": "1", "application_date": "bad"})
    assert errors["application_date"] == "Use YYYY-MM-DD"


def test_salary_order_and_list_json():
    values, errors = validate(RESOURCES["jobs"], {"company_id": "1", "job_title": "X", "job_type": "Contract",
                                                  "salary_min": "100", "salary_max": "50",
                                                  "requirements": "Python, SQL"})
    assert "salary_max" in errors and values["requirements"] == '["Python", "SQL"]'


def test_missing_required():
    _, errors = validate(RESOURCES["companies"], {})
    assert errors == {"company_name": "Required"}
