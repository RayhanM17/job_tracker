"""Turn raw form input into clean DB values, collecting per-field errors."""
import json
from datetime import date

import database
from resources import RESOURCES


def fk_options(resource_key):
    """(id, label) pairs for a foreign-key dropdown."""
    r = RESOURCES[resource_key]
    rows = database.query(f"SELECT {r['pk']} AS id, {r['label_sql']} AS label FROM {r['table']} ORDER BY label")
    return [(row["id"], row["label"]) for row in rows]


def _clean(field, raw, errors):
    name, kind = field["name"], field["kind"]
    raw = (raw or "").strip()
    if kind == "bool":
        return 1 if raw else 0
    if not raw:
        if field["required"]:
            errors[name] = "Required"
        return None
    if field.get("max") and len(raw) > field["max"]:
        errors[name] = f"Max {field['max']} characters"
    try:
        if kind == "int":
            value = int(raw)
            if value < 0:
                raise ValueError
            return value
        if kind == "date":
            return date.fromisoformat(raw).isoformat()
        if kind == "fk":
            return int(raw)
        if kind == "enum":
            if raw not in field["options"]:
                raise ValueError
            return raw
        if kind == "list":
            items = [s.strip() for s in raw.split(",") if s.strip()]
            return json.dumps(items)
        if kind == "json":
            json.loads(raw)
            return raw
    except ValueError:
        errors[name] = {"int": "Enter a non-negative whole number", "date": "Use YYYY-MM-DD",
                        "json": "Invalid JSON"}.get(kind, "Invalid value")
    return raw


def validate(resource, form):
    """Return (values dict, errors dict)."""
    errors, values = {}, {}
    for f in resource["fields"]:
        values[f["name"]] = _clean(f, form.get(f["name"]), errors)
    lo, hi = values.get("salary_min"), values.get("salary_max")
    if isinstance(lo, int) and isinstance(hi, int) and lo > hi:
        errors["salary_max"] = "Must be at least the minimum"
    email = values.get("email")
    if email and "@" not in email:
        errors["email"] = "Invalid email"
    return values, errors


def form_value(field, value):
    """Convert a stored DB value back into what the form input should show."""
    if value is None:
        return ""
    if field["kind"] == "list":
        return ", ".join(json.loads(value) if isinstance(value, (str, bytes)) else value)
    if field["kind"] == "json":
        return value if isinstance(value, str) else json.dumps(value)
    return value
