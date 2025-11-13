# Automated Test Case Generator for Web Forms

A web-based system that automatically parses HTML form structures and generates comprehensive test cases including valid, invalid, boundary, and combinatorial scenarios.

---

## Abstract
This project automates the generation of test cases for HTML-based web forms by analyzing input field constraints such as type, required status, ranges, patterns, and options. It produces valid, invalid, boundary, and security-focused input values and returns a structured JSON output. The system emphasizes performance, reliability, usability, and maintainability through a modular architecture.

---

## Introduction
HTML forms are a core component of most web applications, and validating them thoroughly is essential. Manual test case writing is slow and error-prone. This project parses the structure of any HTML form and automatically generates test cases. It follows a layered architecture separating UI, parsing, and test generation logic to ensure maintainability and scalability.

---

## High-Level Architecture

```plantuml
@startuml
title Automated Test Case Generator - High Level Architecture

skinparam style strictuml
skinparam componentStyle rectangle

rectangle "User Browser" as BROWSER

rectangle "Frontend Layer" {
    component "UI Page (HTML/CSS)\nPaste HTML Form\nButtons: Use Sample, Generate\nOutput Viewer" as UI
    component "Client Script (main.js)\nPOST /generate\nRenders JSON Output" as JS
}

rectangle "Backend Layer (Flask App)" {
    component "/generate API Endpoint" as API
    component "HTML Parser (BeautifulSoup)\nExtracts fields, constraints" as PARSER
    component "Test Case Generator\nValid/Invalid/Boundary/Combinatorial Cases" as ENGINE
    component "JSON Builder" as JSON_OUT
}

rectangle "Output JSON" as OUTPUT

BROWSER --> UI
UI --> JS
JS --> API
API --> PARSER
PARSER --> ENGINE
ENGINE --> JSON_OUT
JSON_OUT --> JS
JS --> BROWSER

@enduml
Tech Stack
Layer	Technology
Frontend	HTML, CSS, JavaScript
Backend	Python (Flask)
Parsing	BeautifulSoup (lxml)
Output	JSON

Project Structure
css
Copy code
automated-form-tester/
│── app.py
│── templates/
│     └── index.html
│── static/
│     ├── main.js
│     ├── style.css
│     └── sample_hint.txt
│── examples/
│     └── sample_form.html
│── README.md
│── requirements.txt
Methodology
1. Parsing Phase
HTML form is parsed using BeautifulSoup.
The system extracts:

Field name

Field type

Required attribute

Min / Max

Minlength / Maxlength

Pattern

Options (select, radio, checkbox)

Handled by: parse_form()

2. Value Generation Phase
For each field:

Valid values

Respect constraints

Fit defined ranges and lengths

Invalid values

Empty input

Too short / too long text

Out-of-range numbers

Incorrect formats

SQL/XSS payloads

Handled by:

generate_valid_value()

generate_invalid_values()

3. Test Case Assembly
The system creates:

Baseline valid test case

Single-field negative test cases

Boundary value tests

Combinatorial test cases (capped using max_combinations)

Handled by: generate_test_cases()

4. Output Construction
Output is a JSON object containing:

fields[] metadata

test_cases[] list with generated inputs

Functional Requirements
Requirement	Description	Code Reference
Form Parsing	Extract field definitions	parse_form()
Valid Input Generation	Generate valid values based on constraints	generate_valid_value()
Invalid/Boundary Input Generation	Generate invalid values	generate_invalid_values()
Test Case Generation	Build complete test suite	generate_test_cases()

Non-Functional Requirements
Attribute	Description	Implementation Detail
Performance	Handles large forms efficiently	max_combinations limit
Reliability	Produces consistent, deterministic results	Pure logical functions
Usability	Simple user interface for easy workflow	Minimal HTML/CSS layout
Maintainability	Modular architecture	Parser, generator, and UI separated

Results
The system successfully generates:

Valid baseline test case

Negative test cases

Boundary tests

Invalid-format tests (email, url, number, etc.)

Security tests (SQL/XSS payloads)

Combinatorial inputs

Field metadata with constraints

Example output structure:
json
Copy code
{
  "fields": [...],
  "test_cases": [...]
}
How to Run
nginx
Copy code
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
python app.py
Open in browser:

cpp
Copy code
http://127.0.0.1:5000/
Contributors
Contributor	Role
Nithin Manoj	Parser development, test generator logic, backend design, documentation
Suresh	UI development, interface workflow, testing, project report

yaml
Copy code

---

If you want a **short version**, **IEEE format**, or **PDF-ready version**, just ask.
