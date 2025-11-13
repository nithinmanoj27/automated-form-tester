"""
Automated Test Case Generator for Web Forms
Flask app that accepts an HTML form (or example file), parses inputs & constraints,
and generates test cases: valid, invalid, boundary, and common security payloads.
"""
from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
from email_validator import validate_email, EmailNotValidError
import re
from typing import List, Dict, Any

app = Flask(__name__, static_folder="static", template_folder="templates")

# ------------------- Helper: Valid & Invalid Values -------------------

def generate_valid_value(field_type, attrs):
    """Return a plausible valid value based on type/attributes."""
    def get_int(k, default=None):
        v = attrs.get(k)
        try:
            return int(v)
        except Exception:
            return default

    if field_type == "email":
        return "user@example.com"
    if field_type in ("number", "range"):
        min_v = get_int("min", 1)
        max_v = get_int("max", (min_v or 0) + 100)
        val = (min_v + max_v) // 2 if (min_v is not None and max_v is not None) else 50
        return str(val)
    if field_type == "tel":
        return "9876543210"
    if field_type == "url":
        return "https://example.com"
    if field_type == "select":
        opts = attrs.get("options")
        if opts and isinstance(opts, list) and len(opts) > 0:
            return opts[0]
        return "option1"
    if field_type == "checkbox":
        return attrs.get("value", "yes")

    # text-like / textarea
    minlength = get_int("minlength", 3)
    maxlength = get_int("maxlength", 20)
    length = max(minlength, 5)
    if maxlength:
        length = min(length, maxlength)
    if length < 1:
        length = 1
    return "a" * length


def generate_invalid_values(field_type, attrs):
    """Return a list of invalid values to test validation (with boundaries and security)."""
    vals = [""]
    def get_int(k, default=None):
        v = attrs.get(k)
        try:
            return int(v)
        except Exception:
            return default

    if field_type == "email":
        vals.extend(["plainaddress", "user@.com", "user@domain"])
    elif field_type == "number":
        vals.append("abc")
        min_v = get_int("min")
        max_v = get_int("max")
        if min_v is not None:
            vals.append(str(min_v - 1))
        if max_v is not None:
            vals.append(str(max_v + 1))
    elif field_type == "url":
        vals.extend(["htp:/bad", "justtext"])
    elif field_type == "select":
        vals.append("INVALID_OPTION")
    elif field_type == "checkbox":
        vals.extend(["", "INVALID", "!!!!!!!!!!!!!!!!!"])
    else:
        maxlength = get_int("maxlength")
        minlength = get_int("minlength")
        if maxlength:
            vals.append("a" * (maxlength + 5))
        if minlength and minlength > 1:
            vals.append("a" * (minlength - 1))
        vals.append("!" * 100)

    # common attack strings
    vals.extend(["' OR '1'='1", "<script>alert(1)</script>", "\" onmouseover=alert(1)"])
    return list(dict.fromkeys(vals))  # remove duplicates


# ------------------- Form Parser -------------------

def parse_form(html_text: str) -> List[Dict[str, Any]]:
    """Parse HTML form and extract all input fields and constraints."""
    soup = BeautifulSoup(html_text, "lxml")
    form = soup.find("form") or soup
    fields = []

    for inp in form.find_all(["input", "textarea", "select"]):
        tag = inp.name
        is_required = "required" in inp.attrs or inp.get("required") is not None

        if tag == "select":
            options = [opt.get("value", opt.text) for opt in inp.find_all("option")]
            fields.append({
                "name": inp.get("name") or inp.get("id") or f"select_{len(fields)}",
                "type": "select",
                "required": is_required,
                "attrs": {"options": options, "required": is_required}
            })
            continue

        ftype = inp.get("type", "text")
        attrs = {
            "required": is_required,
            "minlength": inp.get("minlength"),
            "maxlength": inp.get("maxlength"),
            "min": inp.get("min"),
            "max": inp.get("max"),
            "pattern": inp.get("pattern")
        }

        if ftype in ("checkbox", "radio"):
            attrs["value"] = inp.get("value", "on")

        fields.append({
            "name": inp.get("name") or inp.get("id") or f"{ftype}_{len(fields)}",
            "type": ftype,
            "attrs": {k: v for k, v in attrs.items() if v is not None},
            "required": is_required
        })
    return fields


# ------------------- Safe Test Case Generator -------------------

def generate_test_cases(fields: List[Dict[str, Any]], max_combinations: int = 50) -> List[Dict[str, Any]]:
    """Generate valid, negative, and combinatorial test cases safely (no freeze)."""
    print(f" Generating test cases for {len(fields)} fields...")

    candidates = []
    for f in fields:
        ftype = f.get("type", "text")
        attrs = f.get("attrs", {})
        valid = generate_valid_value(ftype, attrs)
        invalids = generate_invalid_values(ftype, attrs)
        candidates.append({
            "name": f["name"],
            "candidates": [valid] + invalids[:2]  # limit invalids per field
        })

    # baseline valid
    baseline = {c["name"]: c["candidates"][0] for c in candidates}
    test_cases = [{
        "id": "TC-BASE-001",
        "type": "baseline_valid",
        "inputs": baseline,
        "expected": "Accept (server-side validation pass)"
    }]

    # single-field negatives
    tc_id = 2
    for c in candidates:
        for inv in c["candidates"][1:]:
            tc = baseline.copy()
            tc[c["name"]] = inv
            test_cases.append({
                "id": f"TC-NEG-{tc_id:03d}",
                "type": "single_field_negative",
                "bad_field": c["name"],
                "inputs": tc,
                "expected": "Reject (validation error) or safely sanitize"
            })
            tc_id += 1

    # safe lazy combinatorial generation
    def limited_product(lists, limit):
        """Yield combinations lazily, never generating all at once."""
        pools = [tuple(pool) for pool in lists]
        result = [[]]
        for pool in pools:
            result = [x + [y] for x in result for y in pool]
            if len(result) > limit:
                result = result[:limit]
        return result[:limit]

    lists = [c["candidates"][:2] for c in candidates]
    combos = limited_product(lists, max_combinations)

    for i, combo in enumerate(combos, start=1):
        inputs = {candidates[j]["name"]: combo[j] for j in range(len(candidates))}
        test_cases.append({
            "id": f"TC-COMB-{i:03d}",
            "type": "combinatorial",
            "inputs": inputs,
            "expected": "Accept or Reject depending on inputs"
        })

    print(f" Generated {len(test_cases)} test cases safely.")
    return test_cases


# ------------------- Flask Endpoints -------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    print(" /generate route triggered")
    html_text = request.form.get("html_text")
    if not html_text or html_text.strip() == "":
        return jsonify({"error": "No HTML form provided. Please paste a valid form."}), 400

    fields = parse_form(html_text)
    print(f" Parsed {len(fields)} fields from HTML form.")

    test_cases = generate_test_cases(fields)

    if len(test_cases) > 200:
        print(" Truncating output to 200 test cases for performance safety.")
        test_cases = test_cases[:200]

    return jsonify({
        "fields": fields,
        "test_cases": test_cases
    })


if __name__ == "__main__":
    app.run(debug=False, port=5000)
