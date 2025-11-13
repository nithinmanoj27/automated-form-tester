# tests/test_generator.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from app import parse_form, generate_test_cases

def test_parse_and_generate():
    with open("examples/sample_form.html", "r", encoding="utf-8") as f:
        html = f.read()
    fields = parse_form(html)
    assert isinstance(fields, list) and len(fields) >= 4
    tcs = generate_test_cases(fields, max_combinations=10)
    assert any(tc["type"] == "baseline_valid" for tc in tcs)
    assert any(tc["type"] == "single_field_negative" for tc in tcs)
