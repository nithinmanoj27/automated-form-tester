# Automated Test Case Generator for Web Forms

## Overview
This project automatically analyses HTML web forms and generates test cases (valid, invalid, boundary, and security checks) to speed up manual QA testing. It is implemented with Flask (backend) and a simple front-end for quick demonstration.

## Features
- Parses form inputs (input, textarea, select).
- Generates baseline valid case, single-field negative tests, and combinatorial cases.
- Includes common security payloads (SQLi, XSS) for negative tests.
- Exportable JSON output (ready to feed into automated test harnesses).

## Quality Attributes (measured & justified)
- **Usability**: Simple web UI + JSON output. Demonstrated by quick generation in UI and sample outputs in `examples/`.
- **Performance**: Parsing/generation is local and lightweight; combinatorial generation capped (configurable `max_combinations`) to avoid blow-up.
- **Maintainability**: Modular `parse_form` and `generate_test_cases` functions with docstrings; tests in `tests/`.

## Setup (VS Code)
1. Create virtualenv: `python -m venv venv`  
2. Activate it:
   - Windows: `venv\Scripts\activate`
   - Linux/macOS: `source venv/bin/activate`
3. Install: `pip install -r requirements.txt`
4. Run app: `python app.py`  
5. Open `http://127.0.0.1:5000/` in browser.

## How to use
- Paste your form HTML into the textarea and click Generate.
- Or click Generate to use the sample form (server fallback).
- Output JSON shows `fields` and `test_cases`.

## Extending
- Add support for `pattern`, `minlength`, `maxlength` enforcement in the generator.
- Add export to CSV/Excel and a step to run test cases against an endpoint.
